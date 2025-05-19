from expense_classifier.pipeline import Pipeline

if __name__ == '__main__':
    path = input("File path: ")
    code = input("Bank Code: ")
    account = input("Account Name: ")


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

    p = Pipeline(code, store_in_db=True, store_progress=False)

    p.ingest(path, account if account else None, input_cols=input_cols)
    p.transform()
    p.categorize()
    p.file_correction()
    p.publish_data()
