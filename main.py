from expense_classifier.pipeline import Pipeline

if __name__ == '__main__':

    # pipeline = Pipeline('BOB', store_in_db=False, store_progress=False)
    # pipeline.ingest("../datasets/statements/statement_bob.csv", 'BOB Savings')
    # pipeline.transform()
    # pipeline.categorize()
    # pipeline.file_correction()
    # # pipeline.manual_correction()
    # pipeline.publish_data()

    # pipeline2 = Pipeline('PNB', store_in_db=False, store_progress=True)
    # pipeline2.ingest("../2023-24/raw_2023-24.csv", 'PNB Savings')
    # pipeline2.transform()
    # pipeline2.categorize()
    # pipeline2.file_correction()
    # pipeline2.publish_data()

    file='/Users/piyushupreti/Documents/Finance/FY 2025 26/OpTransactionHistoryUX519-05-2025.csv'
    bank='BOB'
    account='BOB Savings'
    date_col = input("Enter date column name (default 'Date'): ") or 'Date'
    credit_col = input("Enter credit column name (default 'Credit'): ") or 'Credit'
    debit_col = input("Enter debit column name (default 'Debit'): ") or 'Debit'
    desc_col = input("Enter description column name (default 'Description'): ") or 'Description'

    input_cols = {
        'date_col': date_col,
        'credit_col': credit_col,
        'debit_col': debit_col,
        'desc_col': desc_col,
    }

    p = Pipeline(bank, store_in_db=False, store_progress=True)
    p.ingest(file, account, input_cols)
    p.transform()
    p.categorize()
    p.file_correction()
    p.publish_data()




    print("Pipeline Completed")

