import re

import pandas as pd

from expense_classifier.utils import get_category_keywords


class Classifier:
    def __init__(self):

        self.category_keywords = get_category_keywords()
        self.category_patterns = {
            category: re.compile('|'.join(map(re.escape, keywords)), re.IGNORECASE)
            if len(keywords) > 0 else None

            for category, keywords in self.category_keywords.items()
        }

    def classify(self, df: pd.DataFrame):
        """Classifies transactions based on predefined rules."""
        df['Category'] = df['Description'].apply(self._apply_rules)
        return df

    def _apply_rules(self, description):
        """Applies classification rules to the transaction description."""

        for category, pattern in self.category_patterns.items():
            if pattern and pattern.search(description):  # Search for any keyword match in the description
                return category
        return 'Uncategorized'
