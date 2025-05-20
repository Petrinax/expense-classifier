import pandas as pd
from datetime import datetime


class CombineData:
    def __init__(self):
        self.combined_data = pd.DataFrame()

    def merge_bank_data(self, df: pd.DataFrame, bank_code: str, account: str):
        """Merges data from different bank files into a single DataFrame."""
        df['Bank'] = bank_code
        df['Account'] = account
        self.combined_data = pd.concat([self.combined_data, df], ignore_index=True)

    def get_data(self):
        """Returns the combined and processed data."""
        return self.combined_data
