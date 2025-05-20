import pandas as pd
from sqlalchemy import create_engine, text

class PaytmLookup:
    def __init__(self, transformed_data: pd.DataFrame, paytm_file_path: str):
        """
        Initialize with categorized transaction data to perform lookup against Paytm data.
        
        :param transformed_data: DataFrame containing categorized transactions
        """
        self.transformed_data = transformed_data
        self.paytm_file_path = paytm_file_path

        self.paytm_data = None
        self.load_paytm_data(file_path=self.paytm_file_path)

        
    def load_paytm_data(self, db_engine=None, file_path=None):
        """
        Load Paytm transaction data either from database or from a file.
        
        :param db_engine: SQLAlchemy engine for database connection
        :param file_path: Path to CSV file containing Paytm data
        :return: PaytmLookup instance for method chaining
        """
        if db_engine:
            # Load data from database table
            query = text("SELECT * FROM paytm_transactions")
            self.paytm_data = pd.read_sql(query, db_engine)
        elif file_path:
            # Load data from CSV file
            if file_path.split(".")[-1] == "csv":
                self.paytm_data = pd.read_csv(file_path)
            elif file_path.split(".")[-1] == "xlsx":
                self.paytm_data = pd.read_excel(file_path, sheet_name='Passbook Payment History')
            else:
                raise ValueError("Unsupported file format. Only CSV and XLSX are allowed.")

        else:
            raise ValueError("Either db_engine or file_path must be provided")
        
        return self

    @staticmethod
    def generate_transaction_text(row):
        mode = row.get('Mode', '')
        payee = row.get('Payee', '')
        payee_account = row.get('Payee Account', '')
        txn_details = row.get('Transaction Details', '')
        remarks = row.get('Remarks', '')
        tags = row.get('Tags', '')
        comment = row.get('Comment', '')
        description = row.get('Description', '')

        text_parts = []
        for text in [description, txn_details, remarks, tags, comment]:
            if pd.notna(text):
                text_parts.append(str(text))

        transaction_text = " ".join(text_parts).lower()

        # transaction_text = (
        #     f"The transaction was made via {mode} to {payee} "
        #     f"({payee_account}). Description: '{txn_details}'. "
        #     f"Remarks: '{remarks}'. Comments: {comment}. Tags include: {tags}."
        # )
        return transaction_text

    def perform_lookup(self):
        """
        Match uncategorized transactions against Paytm data.
        
        :return: DataFrame with updated categories based on Paytm lookup
        """
        if self.paytm_data is None:
            raise ValueError("Paytm data not loaded. Call load_paytm_data first.")
            

        # Create a lookup dictionary from Paytm data
        # Assuming Paytm data has 'Description' and 'Category' columns

        # Convert columns to string type before merging
        self.transformed_data['Txn ID'] = self.transformed_data['Txn ID'].astype(str)
        self.paytm_data['UPI Ref No.'] = self.paytm_data['UPI Ref No.'].astype(str)

        combined_df = pd.merge(
            left=self.transformed_data,
            right=self.paytm_data[['UPI Ref No.', 'Transaction Details', 'Remarks', 'Tags', 'Comment']],
            left_on="Txn ID",
            right_on="UPI Ref No.",
            how="left"
        )

        combined_df['Prompt'] = combined_df.apply(self.generate_transaction_text, axis=1)
        
        return combined_df

