import argparse
from expense_classifier import Pipeline


def parse_arguments():
    parser = argparse.ArgumentParser(description='Classify expenses from bank statements')
    parser.add_argument('--path', '-p', help='Path to the bank statement file')
    parser.add_argument('--bank-code', '-b', help='Bank code')
    parser.add_argument('--account', '-a', help='Account name')
    parser.add_argument('--date-col', default='Date', help='Date column name (default: Date)')
    parser.add_argument('--credit-col', default='Credit', help='Credit column name (default: Credit)')
    parser.add_argument('--debit-col', default='Debit', help='Debit column name (default: Debit)')
    parser.add_argument('--desc-col', default='Description', help='Description column name (default: Description)')
    parser.add_argument('--paytm-lookup', action='store_true', help='Perform Paytm lookup for uncategorized records')
    parser.add_argument('--paytm-file', help='Path to Paytm data file')
    parser.add_argument('--store-in-db', action='store_true', help='Store data in database')
    parser.add_argument('--store-progress', action='store_true', default=True, help='Store progress data')

    return parser.parse_args()


def main(preset_args=None):
    # If preset_args is provided, use them
    # otherwise parse from command line
    if preset_args:
        args = preset_args
    else:
        args = parse_arguments()
    
    if not args.path or not args.bank_code:
        # Interactive mode
        path = input("File path: ")
        code = input("Bank Code: ")
        account = input("Account Name: ")

        date_col = input(f"Enter date column name (default 'Date'): ") or 'Date'
        credit_col = input(f"Enter credit column name (default 'Credit'): ") or 'Credit'
        debit_col = input(f"Enter debit column name (default 'Debit'): ") or 'Debit'
        desc_col = input(f"Enter description column name (default 'Description'): ") or 'Description'

        # Ask if user wants to perform Paytm lookup
        paytm_lookup = input("Perform Paytm lookup for uncategorized records? (y/n, default: n): ").lower() == 'y'
        paytm_file_path = None
        if paytm_lookup:
            paytm_file_path = input("Enter Paytm data file path: ")

        # Ask for database and progress storage preferences
        store_in_db = input("Store data in database? (y/n, default: n): ").lower() == 'y'
        store_progress = input("Store progress data? (y/n, default: y): ").lower() != 'n'
    else:
        # Command-line mode
        path = args.path
        code = args.bank_code
        account = args.account
        date_col = args.date_col
        credit_col = args.credit_col
        debit_col = args.debit_col
        desc_col = args.desc_col
        paytm_lookup = args.paytm_lookup
        paytm_file_path = args.paytm_file
        store_in_db = args.store_in_db
        store_progress = args.store_progress

    input_cols = {
        'date_col': date_col,
        'credit_col': credit_col,
        'debit_col': debit_col,
        'desc_col': desc_col,
    }

    p = Pipeline(code, store_in_db=store_in_db, store_progress=store_progress, file_path=path, account_name=account, input_cols=input_cols, paytm_lookup=paytm_lookup, paytm_file_path=paytm_file_path)

    p.ingest()
    p.transform()
    p.join_paytm()
    p.categorize()

    
    p.file_correction()
    # p.add_fiscal_period()
    final_df , final_table, final_path = p.publish_data()
    
    return final_path


if __name__ == '__main__':
    main()
