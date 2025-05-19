import re

import pandas as pd

from expense_classifier.bank_utils import bank_codes, Bank


class Transformer:
    def __init__(self, df: pd.DataFrame, bank: Bank, account_name):
        self.df = df
        self.bank = bank
        self.account_name = account_name

    def transform(self):

        # Add Payment Mode and Payee Details
        self.df[['Mode', 'Payee Account', 'Payee']] = self.df['Description'].apply(self.extract_transaction_details)

        # Add the 'group' column based on conditions
        self.df['Group'] = self.df['Amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')

        self.df['Account'] = self.account_name

        return self.df

    def extract_transaction_details(self, description):

        # Extract Mode (first part before the first '/')
        mode = str(description.split('/')[0]).lower()
        payee_account = ''
        payee = ''

        if mode == 'upi':
            # Extract Payee Account (the part after the second-last '/' )
            upi_pattern = self.bank.upi_regex_pattern
            if upi_pattern:
                match = re.search(upi_pattern, description)
                if match:
                    groups = match.groupdict()
                    payee_account = groups.get('upi_id')
                    payee = groups.get('payee')

            # Commented to prevent print statements for every record.
            # else:
            #

        elif mode == 'npci':
            # Extract Payee (the part after the last '/' )
            payee = description.split('/')[-1]
        elif mode == 'nach':
            # Extract Payee (the part after the last '/' )
            payee = description.split('/')[-1]
        elif len(mode) > 10:
            mode = None


        return pd.Series([mode, payee_account, payee], index=['Mode', 'Payee Account', 'Payee'])

