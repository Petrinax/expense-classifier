from datetime import datetime
from expense_classifier.manual_correction import ManualCorrection
from expense_classifier.transformer import Transformer
from expense_classifier.ingestor import Ingestor
from expense_classifier.classifier import Classifier
from sqlalchemy import create_engine
import os

today = datetime.now().date().isoformat()
with open('../local_files/sql_alchemy_url.txt') as f:
    db_url = f.read()
engine = create_engine(db_url)

def main():
    file_path = f"../datasets/sample_data.csv"
    data = Ingestor(file_path).get_data()
    data.to_csv('../datasets/raw_data.csv')
    data.to_sql(f"raw_data_{today}", con=engine, if_exists='replace')


    transformed_data = Transformer(data).transform()
    transformed_data.to_csv('../datasets/transformed_data.csv')
    transformed_data.to_sql(f"transformed_data_{today}", con=engine, if_exists='replace')



    categorized_data = Classifier().classify(transformed_data)
    categorized_data.to_csv('../datasets/categorized_data.csv')
    categorized_data.to_sql(f"categorized_data_{today}", con=engine, if_exists='replace')

    # if input("Review for manual corrections (Y/n)?").lower() == 'y':
    manually_corrected_data = ManualCorrection(categorized_data).get_data()
    manually_corrected_data.to_csv('../datasets/manually_corrected_data.csv')
    manually_corrected_data.to_sql(f"manually_corrected_data_{today}", con=engine, if_exists='replace')



if __name__ == '__main__':
    main()
