import os
import pandas as pd
from expense_classifier.pipeline import Pipeline
from expense_classifier.combine import CombineData
from expense_classifier.transformer import Transformer
from expense_classifier.bank_utils import bank_codes
from datetime import datetime
from reporting.generator import generate_comprehensive_report

def run_pipeline(path, bank_code, account_name, paytm_file=None, paytm_lookup=False, 
                date_col='Date', credit_col='Credit', debit_col='Debit', 
                desc_col='Description', store_in_db=False, store_progress=True,
                 output_path=None):
    """
    Run the expense classification pipeline for a single bank statement
    """
    print(f"Processing {account_name} statement...")
    
    # Configure input columns
    input_cols = {
        'date_col': date_col,
        'credit_col': credit_col,
        'debit_col': debit_col,
        'desc_col': desc_col,
    }
    
    # Initialize pipeline
    pipeline = Pipeline(
        bank_code=bank_code,
        store_in_db=store_in_db,
        store_progress=store_progress,
        file_path=path,
        account_name=account_name,
        input_cols=input_cols,
        paytm_lookup=paytm_lookup,
        paytm_file_path=paytm_file,
        output_directory=output_path
    )
    
    # Run pipeline steps
    pipeline.ingest()
    pipeline.transform()
    
    pipeline.join_paytm()
    
    pipeline.categorize()
    pipeline.file_correction()
    
    # Get the final DataFrame
    df, _, _ = pipeline.publish_data(table_name=f"{account_name}_processed")
    
    return df, bank_code, account_name

def main():
    # Define base path and common files
    base_path = "/Users/piyushupreti/Documents/Finance/FY 2024-25/all data/raw"
    output_path = "/Users/piyushupreti/Documents/Finance/FY 2024-25/all data/reports"
    paytm_file = f"{base_path}/Paytm_UPI_Statement_01_Apr'24_-_31_Mar'25.xlsx"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Define bank statement configurations
    bank_configs = [
        {
            'path': f"{base_path}/BOB_2024-25.csv",
            'bank_code': "BOB",
            'account_name': "BOB Savings",
            'paytm_lookup': True,
            'paytm_file': paytm_file,
        },
        {
            'path': f"{base_path}/PNB_2024-25.csv",
            'bank_code': "PNB",
            'account_name': "PNB Savings",
            'paytm_lookup': True,
            'paytm_file': paytm_file,
        },
        {
            'path': f"{base_path}/SBI_1_2024-25.csv",
            'bank_code': "SBI",
            'account_name': "SBI Savings 1",
            'paytm_lookup': True,
            'paytm_file': paytm_file,
        },
        {
            'path': f"{base_path}/SBI_2_2024-25.csv",
            'bank_code': "SBI",
            'account_name': "SBI Savings 2",
            'paytm_lookup': True,
            'paytm_file': paytm_file,
        }
    ]
    
    # Initialize CombineData object
    combiner = CombineData()
    
    # Process each bank statement and combine the results
    for config in bank_configs:
        df, bank_code, account_name = run_pipeline(**config)
        combiner.merge_bank_data(df, bank_code, account_name)
    
    # Get the combined data
    combined_data = combiner.get_data()
    
    # Add fiscal periods to the combined data
    combined_data = Transformer.add_fiscal_period(combined_data)
    
    # Generate timestamp for report filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save the combined report
    combined_report_path = f"{output_path}/combined_financial_report_{timestamp}.csv"
    combined_data.to_csv(combined_report_path, index=False)
    print(f"Combined report saved to: {combined_report_path}")
    
    # Generate comprehensive reports and visualizations
    reports = generate_comprehensive_report(combined_data, output_path)
    
    print("All reports and visualizations generated successfully!")
    
    return combined_data

if __name__ == "__main__":
    main()