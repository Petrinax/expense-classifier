import pandas as pd


class Ingestor:
    def __init__(self, file_path: str):

        self.file_path = file_path
        self.date_col = 'Date'
        self.amount_col = 'Amount'
        self.credit_col = 'Credit'
        self.debit_col = 'Debit'
        self.desc_col = 'Description'

        self.df = self.load_data()
        self.invalid_records = pd.DataFrame()
        self.clean_data()

    def load_data(self) -> pd.DataFrame:
        """Loads account statement data from CSV or Excel."""
        if self.file_path.endswith('.csv'):
            return pd.read_csv(self.file_path)
        elif self.file_path.endswith('.xlsx'):
            return pd.read_excel(self.file_path)
        else:
            raise ValueError("Unsupported file format. Only CSV and XLSX are allowed.")

    def clean_data(self):
        """
        Cleans the data
        - Extract transactional columns (e.g., date, description, amount).
        """
        # Validate that only one of 'credit' or 'debit' has a value
        self.df['valid'] = ((self.df['Credit'].notna() & self.df['Debit'].isna()) | (
                self.df['Credit'].isna() & self.df['Debit'].notna()))

        self.invalid_records = self.df[~self.df['valid']]
        self.df = self.df[self.df['valid']]

        self.df[self.credit_col] = self.df[self.credit_col].str.replace(r'[^\d.-]', '', regex=True).str.strip()

        self.df[self.debit_col] = self.df[self.debit_col].str.replace(r'[^\d.-]', '', regex=True).str.strip()

        self.df[self.credit_col] = pd.to_numeric(self.df[self.credit_col], errors='coerce').fillna(0)
        self.df[self.debit_col] = pd.to_numeric(self.df[self.debit_col], errors='coerce').fillna(0)

        # Create 'amount' column by subtracting 'debit' from 'credit'
        self.df[self.amount_col] = self.df[self.credit_col] - self.df[self.debit_col]
        self.df = self.df[[self.date_col, self.amount_col, self.desc_col]]

        # self.df[self.date_col] = pd.to_datetime(self.df[self.date_col], errors='coerce')  # Standardize date format

        self.df[self.desc_col] = self.df[self.desc_col].str.lower()

    def get_data(self):
        return self.df
