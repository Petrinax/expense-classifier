import re

import pandas as pd


class Transformer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def transform(self):

        # Add Payment Mode and Payee Details
        self.df[['Mode', 'Payee Account', 'Payee']] = self.df['Description'].apply(self.extract_transaction_details)

        # Add the 'group' column based on conditions
        self.df['Group'] = self.df['Amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')

        self.df['Account'] = 'PNB Savings'

        return self.df

    @staticmethod
    def extract_transaction_details(description):
        # Extract Mode (first part before the first '/')

        mode = str(description.split('/')[0]).lower()
        payee_account = ''
        payee = ''

        if mode == 'upi':
            # Extract Payee Account (the part after the second-last '/' )
            payee_account = description.split('/')[-2]

            # Extract Payee (the part after the last '/' )
            payee = description.split('/')[-1]

        elif mode == 'npci':
            # Extract Payee (the part after the last '/' )
            payee = description.split('/')[-1]

        return pd.Series([mode, payee_account, payee], index=['Mode', 'Payee Account', 'Payee'])

