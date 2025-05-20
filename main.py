from expense_classifier.pipeline import Pipeline
from expense_classifier.bank_utils import bank_codes
from expense_classifier.main import main as expense_classifier_main
import pandas as pd
import sys
import argparse
import os

def setup_and_run_classifier(path, bank_code, account_name, 
                            date_col='Date', credit_col='Credit', 
                            debit_col='Debit', desc_col='Description',
                            paytm_lookup=False, paytm_file=None, store_in_db=False, store_progress=False,):
    """
    Setup and run the expense classifier for a bank statement
    """
    # Create arguments namespace to simulate command line args
    args = argparse.Namespace(
        path=path,
        bank_code=bank_code,
        account=account_name,
        date_col=date_col,
        credit_col=credit_col,
        debit_col=debit_col,
        desc_col=desc_col,
        paytm_lookup=paytm_lookup,
        paytm_file=paytm_file,
        store_in_db=store_in_db,
        store_progress=store_progress,
    )
    
    # Override sys.argv to prevent argparse from parsing actual command line
    sys.argv = [sys.argv[0]]
    
    # Call the main function with our arguments
    expense_classifier_main(args)

if __name__ == '__main__':
    # Define paths and parameters for each bank
    base_path = "/Users/piyushupreti/Documents/Finance/FY 2024-25/all data/raw"

    paytm_file = f"{base_path}/Paytm_UPI_Statement_01_Apr'24_-_31_Mar'25.xlsx"

    bob = {
        'path': f"{base_path}/BOB_2024-25.csv",
        'bank_code': "BOB",
        'account_name': "BOB Savings",
        'paytm_lookup': True,
        'paytm_file': paytm_file,
        # 'store_in_db': False,
        # 'store_progress': True
    }

    pnb = {
        'path': f"{base_path}/PNB_2024-25.csv",
        'bank_code': "PNB",
        'account_name': "PNB Savings",
        'paytm_lookup': True,
        'paytm_file': paytm_file,
        # 'store_in_db': False,
        # 'store_progress': True
    }

    sbi_1 = {
        'path': f"{base_path}/SBI_1_2024-25.csv",
        'bank_code': "SBI",
        'account_name': "SBI Savings 1",
        'paytm_lookup': True,
        'paytm_file': paytm_file,
        # 'store_in_db': False,
        # 'store_progress': True
    }

    sbi_2 = {
        'path': f"{base_path}/SBI_2_2024-25.csv",
        'bank_code': "SBI",
        'account_name': "SBI Savings 2",
        'paytm_lookup': True,
        'paytm_file': paytm_file,
        # 'store_in_db': False,
        # 'store_progress': True
    }

    # # Process each bank statement
    print("Processing BOB statement...")
    setup_and_run_classifier(**bob)
    # 
    print("Processing PNB statement...")
    setup_and_run_classifier(**pnb)
    # 
    print("Processing SBI 1 statement...")
    setup_and_run_classifier(**sbi_1)

    print("Processing SBI 2 statement...")
    setup_and_run_classifier(**sbi_2)
    
    print("All bank statements processed successfully!")

