import re

import pandas as pd

from expense_classifier.bank_utils import bank_codes, Bank


class Transformer:
    def __init__(self, df: pd.DataFrame, bank: Bank, account_name):
        self.df = df
        self.bank = bank
        self.account_name = account_name

    def transform(self):

        # # Add Fiscal Period
        # self.df = self.add_fiscal_period(self.df)

        # Add Payment Mode and Payee Details
        self.df[['Mode', 'Payee Account', 'Payee', 'Txn ID']] = self.df['Description'].apply(self.extract_transaction_details)

        # Add the 'group' column based on conditions
        self.df['Group'] = self.df['Amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')

        self.df['Account'] = self.account_name

        return self.df

    @staticmethod
    def add_fiscal_period(df):

        # Fiscal year starts in April
        fiscal_year_start_month = 4

        # Calendar components
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day

        # Fiscal Year
        df['Fiscal_Year'] = df['Date'].apply(lambda x: x.year if x.month >= fiscal_year_start_month else x.year - 1)

        # Fiscal Period (1 = April, ..., 12 = March)
        df['Fiscal_Period'] = df['Date'].apply(lambda x: (x.month - fiscal_year_start_month) % 12 + 1)

        # Fiscal Month (e.g., Jan-25)
        df['Fiscal_Month'] = df['Date'].dt.strftime('%b-%y')

        # Reuse Fiscal_Period to get Fiscal Quarter No (1–4)
        df['Quarter No'] = ((df['Fiscal_Period'] - 1) // 3) + 1
        df['Quarter'] = 'Q' + df['Quarter No'].astype(str)
        return df

    def extract_transaction_details(self, description):

        # Extract Mode (first part before the first '/')
        mode = str(description.split('/')[0]).lower()
        payee_account = ''
        payee = ''
        txn_id = ''

        # if mode is upi
        if re.search(r"^[^/]*\b(?P<mode>upi)$", mode, re.IGNORECASE):
            mode = 'upi'
            # Extract Payee Account (the part after the second-last '/' )
            upi_pattern = self.bank.upi_regex_pattern
            if upi_pattern:
                match = upi_pattern.search(description)
                if match:
                    groups = match.groupdict()
                    payee_account = groups.get('upi_id', '')
                    payee = groups.get('payee', '')
                    txn_id = groups.get('upi_ref_no', '')

        # todo: Change condition for SBI (not currently generic)
        elif mode == 'npci':
            # Extract Payee (the part after the last '/' )
            payee = description.split('/')[-1]
        elif mode == 'nach':
            # Extract Payee (the part after the last '/' )
            payee = description.split('/')[-1]
        elif len(mode) > 20:
            mode = None


        return pd.Series([mode, payee_account, payee, txn_id], index=['Mode', 'Payee Account', 'Payee', 'Txn ID'])

