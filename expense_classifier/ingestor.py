import pandas as pd


class Ingestor:
    def __init__(self, file_path: str, date_col: str = 'Date', credit_col: str = 'Credit', debit_col: str = 'Debit', desc_col: str = 'Description'):

        self.file_path = file_path

        self.date_col = date_col
        self.credit_col = credit_col
        self.debit_col = debit_col
        self.desc_col = desc_col

        self.amount_col = 'Amount'

        self.data_types = {
            self.date_col: 'string',
            self.credit_col: 'string',
            self.debit_col: 'string',
            self.desc_col: 'string'
        }

        self.df = self.load_data()
        self.invalid_records = pd.DataFrame()
        self.clean_data()

    def load_data(self) -> pd.DataFrame:
        """Loads account statement data from CSV or Excel."""
        if self.file_path.endswith('.csv'):
            return pd.read_csv(self.file_path, dtype=self.data_types)
        elif self.file_path.endswith('.xlsx'):
            return pd.read_excel(self.file_path, dtype=self.data_types)
        else:
            raise ValueError("Unsupported file format. Only CSV and XLSX are allowed.")

    def clean_data(self):
        """
        Cleans the data
        - Extract transactional columns (e.g., date, description, amount).
        """
        # Format DateTime
        self.df[self.date_col] = pd.to_datetime(self.df[self.date_col], dayfirst=True).dt.date

        # Validate that only one of 'credit' or 'debit' has a value
        self.df['valid'] = ((self.df[self.credit_col].notna() & self.df[self.debit_col].isna()) | (
                self.df[self.credit_col].isna() & self.df[self.debit_col].notna()))

        self.invalid_records = self.df[~self.df['valid']]
        self.df = self.df[self.df['valid']]

        self.df[self.credit_col] = self.df[self.credit_col].str.replace(r'[^\d.-]', '', regex=True).str.strip()

        self.df[self.debit_col] = self.df[self.debit_col].str.replace(r'[^\d.-]', '', regex=True).str.strip()

        self.df[self.credit_col] = pd.to_numeric(self.df[self.credit_col], errors='coerce').fillna(0)
        self.df[self.debit_col] = pd.to_numeric(self.df[self.debit_col], errors='coerce').fillna(0)

        # Create 'amount' column by subtracting 'debit' from 'credit'
        self.df[self.amount_col] = self.df[self.credit_col] - self.df[self.debit_col]

        # Rename columns to default names
        self.df = self.df.rename(columns={
            self.date_col: 'Date',
            self.credit_col: 'Credit',
            self.debit_col: 'Debit',
            self.desc_col: 'Description'
        })
        self.df = self.df[['Date', 'Credit', 'Debit', self.amount_col, 'Description']]

        self.df[self.desc_col] = self.df[self.desc_col].str.lower()

    def get_data(self):
        return self.df
