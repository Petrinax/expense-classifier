from collections import Counter

import pandas as pd

from db_utils import get_category_keywords, add_keywords

pd.set_option('display.max_colwidth', None)


class ManualCorrection:
    ALL_CATEGORIES: dict = get_category_keywords()

    def __init__(self, data: pd.DataFrame):
        self.df = data
        self.uncategorized_df: pd.DataFrame = self.get_uncategorized_transactions()
        self.top_col_value, self.top_count, self.count_col_name = (None, None, None)
        self.update_categories()

    def update_categories(self):
        """
        Allow manual category correction for individual transactions.
        - Update the transaction category in the database
        - Prompt user for manual corrections
        """

        print("\n--- Manual Correction ---")
        while len(self.uncategorized_df):
            self.top_col_value, self.top_count, self.count_col_name = self.update_field_count()
            print("\n Top Uncategorized Transaction:")
            print(f"{self.top_col_value} -> {self.top_count} transactions")

            transaction: pd.Series = self.uncategorized_df.drop(columns=[self.count_col_name]).iloc[0]

            self.record_correction(transaction)

    def update_field_count(self):

        column = 'Payee Account'
        count_col_name = f'{column} Count'
        counts = Counter(self.uncategorized_df[column])
        # print(f"\nTop uncategorized Payees:")
        for value, count in counts.items():
            self.uncategorized_df.loc[self.uncategorized_df[column] == value, count_col_name] = count

        self.uncategorized_df = self.uncategorized_df.sort_values(by=[count_col_name], ascending=False)
        top_col_value, top_count = counts.most_common(1)[0]
        return top_col_value, top_count, count_col_name

    def record_correction(self, transaction: pd.Series):

        print("Transaction Details: ")
        print(transaction.to_string())
        filter_column = 'Payee Account'
        filter_value = transaction[filter_column]
        old_category = transaction['Category']

        while True:
            new_category = input("Enter new category for this transaction (or leave blank to skip): ").strip()
            if new_category and not self.ALL_CATEGORIES.get(new_category):
                print(f"Invalid category provided. "
                      f"Accepted values: \n {list(self.ALL_CATEGORIES.keys())}")
            else:
                break

        apply_all = input(f"Apply to all transactions with {filter_column}: {filter_value} (Y/n)?").lower() == 'y'
        if apply_all:
            condition = ((self.uncategorized_df[filter_column] == filter_value) &
                         (self.uncategorized_df['Category'] == old_category))
        else:
            condition = (self.uncategorized_df.index == transaction.name)

        record_count = len(self.uncategorized_df.loc[condition])
        indices = self.uncategorized_df[condition].index

        if new_category:

            self.df.loc[indices, 'Category'] = new_category
            print(f"Updated {record_count} record(s) with {new_category} category. ")

            remember = input(f"Remember to map transactions with {filter_column} = {filter_value}"
                             f"with Category = {new_category} (Y/n)?").lower() == 'y'
            if remember:
                add_keywords(new_category, filter_column, filter_value)

        self.uncategorized_df.drop(index=indices, inplace=True)

    def get_uncategorized_transactions(self):
        """Get transactions that were not automatically classified, awaiting manual correction."""
        return self.df[self.df['Category'] == 'Uncategorized']

    def get_data(self):
        return self.df
