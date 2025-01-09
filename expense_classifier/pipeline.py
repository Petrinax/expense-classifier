from datetime import datetime

import pandas as pd

from expense_classifier.file_correction import FileCorrection
from expense_classifier.manual_correction import ManualCorrection
from expense_classifier.transformer import Transformer
from expense_classifier.ingestor import Ingestor
from expense_classifier.classifier import Classifier
from sqlalchemy import create_engine

today = datetime.now().date().isoformat()
fin_month = datetime.now().strftime('%Y-%m')

with open('/Users/piyushupreti/Documents/Projects/expense-classifier/local_files/sql_alchemy_url.txt') as f:
    db_url = f.read()
engine = create_engine(db_url)


FILE_PATH = "/Users/piyushupreti/Documents/Projects/expense-classifier/datasets/sample_data.csv"


class Pipeline:
    data: pd.DataFrame

    def ingest(self, file_path: str = FILE_PATH):
        self.raw_data = Ingestor(file_path).get_data()
        self.raw_data.to_csv('../datasets/raw_data.csv')
        # self.raw_data.to_sql(f"raw_data_{today}", con=engine, if_exists='replace')
        self.data = self.raw_data

    def transform(self):
        self.transformed_data = Transformer(self.data).transform()
        self.transformed_data.to_csv('../datasets/transformed_data.csv')
        # self.transformed_data.to_sql(f"transformed_data_{today}", con=engine, if_exists='replace')
        self.data = self.transformed_data

    def categorize(self):
        self.categorized_data = Classifier().classify(self.data)
        self.categorized_data.to_csv('../datasets/categorized_data.csv')
        # self.categorized_data.to_sql(f"categorized_data_{today}", con=engine, if_exists='replace')

        self.uncategorized_data = self.categorized_data[self.categorized_data['Category'] == 'Uncategorized']
        self.uncategorized_data.to_csv('../datasets/uncategorized_data.csv')

        self.data = self.categorized_data

    def manual_correction(self):
        # if input("Review for manual corrections (Y/n)?").lower() == 'y':
        self.manually_corrected_data = ManualCorrection(self.data).get_data()
        self.manually_corrected_data.to_csv('../datasets/manually_corrected_data.csv')
        # self.manually_corrected_data.to_sql(f"manually_corrected_data_{today}", con=engine, if_exists='replace')
        self.data = self.manually_corrected_data

    def file_correction(self):
        self.file_corrected_data = FileCorrection(self.data).get_date()
        self.file_corrected_data.to_csv('../datasets/file_corrected_data.csv')
        # self.file_corrected_data.to_sql(f"file_corrected_data_{today}", con=engine, if_exists='replace')
        self.data = self.file_corrected_data

    def publish_data(self, table_name=f"Transactions_{today}"):
        self.data.to_sql(table_name, con=engine, if_exists='replace')


