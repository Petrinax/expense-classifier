import uuid
from datetime import datetime
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine

from expense_classifier.bank_utils import bank_codes, Bank
from expense_classifier.classifier import Classifier
from expense_classifier.file_correction import FileCorrection
from expense_classifier.ingestor import Ingestor
from expense_classifier.manual_correction import ManualCorrection
from expense_classifier.transformer import Transformer

today = datetime.now().date().isoformat()
fin_month = datetime.now().strftime('%Y-%m')

with open('/Users/piyushupreti/Documents/Projects/expense-classifier/local_files/sql_alchemy_url.txt') as f:
    db_url = f.read()

engine = create_engine(db_url)


FILE_PATH = "/Users/piyushupreti/Documents/Projects/expense-classifier/datasets/sample_data.csv"


class Pipeline:
    data: pd.DataFrame

    def __init__(self, bank_code: str, store_in_db: bool = False, store_progress: bool = False):
        """
        :param bank_code: Bank Code for fields extraction
        :param store_in_db: If set to True, will store data to db as well.
        :param store_progress: If set to True, will save intermediate transformation results to file.
        Note: if store_id_db is set to true with this, it'll store transformed data in db as well.
        """


        self.bank_code = bank_code
        self.bank = bank_codes.get(self.bank_code)
        if not self.bank:
            print(f"Bank code {self.bank_code} not registered. Some features may not work correctly."
                  f"\nList of valid bank codes: \n{list(bank_codes.keys())}")
            self.bank = Bank(code=bank_code, name=bank_code, upi_regex_pattern=None)
        self.store_in_db = store_in_db,
        self.store_progress = store_progress

        self.file_directory = None
        self.file_name = None
        self.account_name = None
        self.raw_data: Optional[pd.DataFrame] = None
        self.transformed_data: Optional[pd.DataFrame] = None
        self.categorized_data: Optional[pd.DataFrame] = None
        self.uncategorized_data: Optional[pd.DataFrame] = None
        self.file_corrected_data: Optional[pd.DataFrame] = None
        self.manually_corrected_data: Optional[pd.DataFrame] = None

    def ingest(self, file_path: str = FILE_PATH, account_name: str = None, input_cols = {}):

        self.account_name = account_name if account_name else f"{self.bank.code}"
        self.raw_data = Ingestor(file_path, **input_cols).get_data()
        self.file_directory , self.file_name = file_path.rsplit('/', maxsplit=1)

        if self.store_progress:
            self.raw_data.to_csv(f'{self.file_directory}/raw_{self.file_name}')
            if self.store_in_db:
                self.raw_data.to_sql(f"raw_data_{today}", con=engine, if_exists='replace')

        self.data = self.raw_data

    def transform(self):

        self.transformed_data = Transformer(self.data, self.bank, self.account_name).transform()

        if self.store_progress:
            self.transformed_data.to_csv(f'{self.file_directory}/transformed_{self.file_name}')
            if self.store_in_db:
                self.transformed_data.to_sql(f"transformed_data_{today}", con=engine, if_exists='replace')
        self.data = self.transformed_data

    def categorize(self):

        self.categorized_data = Classifier().classify(self.data)

        self.uncategorized_data = self.categorized_data[self.categorized_data['Category'] == 'Uncategorized']

        if self.store_progress:
            self.categorized_data.to_csv(f'{self.file_directory}/categorized_{self.file_name}')
            self.uncategorized_data.to_csv(f'{self.file_directory}/uncategorized_{self.file_name}')
            if self.store_in_db:
                self.categorized_data.to_sql(f"categorized_data_{today}", con=engine, if_exists='replace')
                self.categorized_data.to_sql(f"uncategorized_data_{today}", con=engine, if_exists='replace')
        self.data = self.categorized_data

    def manual_correction(self):
        """Not in Use."""
        # if input("Review for manual corrections (Y/n)?").lower() == 'y':
        self.manually_corrected_data = ManualCorrection(self.data).get_data()
        self.manually_corrected_data.to_csv(f'{self.file_directory}/manually_corrected_{self.file_name}')
        # self.manually_corrected_data.to_sql(f"manually_corrected_data_{today}", con=engine, if_exists='replace')
        self.data = self.manually_corrected_data

    def file_correction(self):

        correction_file_name = f"{self.file_directory}/uncategorized_file_correction_{self.file_name}"

        self.file_corrected_data = FileCorrection(self.data, correction_file_name).get_date()

        if self.store_progress:
            self.file_corrected_data.to_csv(f'{self.file_directory}/file_corrected_{self.file_name}')
            if self.store_in_db:
                self.file_corrected_data.to_sql(f"file_corrected_data_{today}", con=engine, if_exists='replace')

        self.data = self.file_corrected_data

    def publish_data(self, table_name=None):
        table = table_name if table_name else f"{self.account_name}_{today}"

        # self.data.drop()
        self.data.to_csv(f'{self.file_directory}/{table}.csv', index=False)
        self.data.to_sql(table, con=engine, if_exists='replace', index=False)

