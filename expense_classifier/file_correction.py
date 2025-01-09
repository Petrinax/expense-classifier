import pandas as pd

from db_utils import get_category_keywords, update_keywords


class FileCorrection:
    FILE_NAME = "/Users/piyushupreti/Documents/Projects/expense-classifier/datasets/uncategorized_data_correction.csv"
    ALL_CATEGORIES: dict = get_category_keywords()

    def __init__(self, data: pd.DataFrame):
        self.df = data
        self.uncategorized_df: pd.DataFrame = self.df[self.df['Category'] == 'Uncategorized'].copy()
        self.already_categorized_data: pd.DataFrame = self.df[self.df['Category'] != 'Uncategorized']
        self.categories = list(self.ALL_CATEGORIES.keys())
        self.category_map: dict[str, set] = {c: set() for c in self.categories}
        self.create_file_from_uncategorized_data()
        self.get_records_with_correction()
        self.process_corrected_file()
        self.review_and_update_category_mappings()
        self.update_source_df()


    def create_file_from_uncategorized_data(self):
        self.uncategorized_df['Keyword'] = ''
        self.uncategorized_df['Category'] = ''
        self.uncategorized_df.to_csv(self.FILE_NAME)

    def get_most_used_categories(self):
        self.category_count: dict = self.already_categorized_data['Category'].value_counts(sort=True, ascending=False).to_dict()
        sorted_categories = list(self.category_count.keys())

        for c in self.categories:
            if c not in sorted_categories:
                sorted_categories.append(c)
        return sorted_categories

    def get_records_with_correction(self):
        sorted_categories = self.get_most_used_categories()
        instructions = f"""
                Instructions:

                - File created for unrecognized data. Path: {self.FILE_NAME}.
                - Update the categories for relevant records. (Skip those you are unsure of).
                - Additionally you can add keywords to look for that particular category.

                """
        valid_categories_by_count = '\n- '.join(['List of accepted Categories [Case Sensitive]:\n'] + sorted_categories)
        instructions_2 = """
        
                - Edit the same file in same location with valid category. Once completed, press 'p'.
                - Press any other key to cancel the step.
                
        """
        print(instructions)
        print(valid_categories_by_count)
        completion_flag = input(instructions_2)
        if completion_flag.lower() != 'p':
            raise KeyboardInterrupt(" File correction step cancelled manually. Exiting pipeline.")

        self.corrected_df = pd.read_csv(self.FILE_NAME, index_col=0)
        self.corrected_df = self.corrected_df.dropna(subset=['Category'])
        print("get_records_with_correction COMPLETED")


    def process_corrected_file(self):
        """ use newly updated self.corrected_df to
        map category to 'Keyword'.
        if 'Keyword' is Null, map category to 'Payee Account'.
        if 'Payee Account' is Null, map category to 'Payee'.
        else map category to 'Description'
        """
        for index, row in self.corrected_df.iterrows():
            if pd.isnull(row['Category']):
                continue
            if pd.isnull(row['Keyword']):
                if pd.isnull(row['Payee Account']):
                    if pd.isnull(row['Payee']):
                        continue
                    else:
                        self.category_map[row['Category']].add(row['Payee'])
                else:
                    self.category_map[row['Category']].add(row['Payee Account'])
            else:
                self.category_map[row['Category']].add(row['Keyword'])

    def review_and_update_category_mappings(self):

        print("Extracted Keywords from corrected file:")
        extracted_keywords: list[tuple] = list(self.category_map.items())
        print('\n'.join([f"{entry[0]}: {entry[1]}" for entry in extracted_keywords]))
        if input("Do you want to map these keywords for future classification? (Y/n)").lower() == 'y':
            update_keywords(self.category_map)

    def update_source_df(self):
        df_cleaned = self.corrected_df.dropna(subset=['Category'])
        self.df.loc[df_cleaned.index, 'Category'] = df_cleaned['Category']

    def get_date(self):
        return self.df








