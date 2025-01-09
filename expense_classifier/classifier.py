import re
from typing import Pattern, Optional
import pandas as pd

from expense_classifier.db_utils import get_category_keywords


class Classifier:
    def __init__(self):

        self.category_keywords = get_category_keywords()
        self.category_patterns: dict[str, Optional[Pattern]] = {}

        for category, keywords in self.category_keywords.items():
            if len(keywords) > 0:
                # Sort keywords to prioritize longer keywords if keyword substrings overlaps
                keywords: list[str] = sorted(keywords, key=len, reverse=True)
                pattern = re.compile('|'.join(map(re.escape, keywords)), re.IGNORECASE)
                self.category_patterns[category] = pattern
            else:
                self.category_patterns[category] = None

    def classify(self, df: pd.DataFrame):
        """Classifies transactions based on predefined rules."""
        df['Category'] = df['Description'].apply(self._apply_rules)
        return df

    def _apply_rules(self, description):
        """Applies classification rules to the transaction description."""

        matches = {}
        for category, pattern in self.category_patterns.items():
            if pattern and pattern.search(description):  # Search for any keyword match in the description
                m = pattern.search(description)
                matched_kw = m.string[m.start():m.end()]
                matches[category] = matched_kw

        if matches:
            longest_matched_keyword = sorted(matches.items(), key=lambda x: len(x[1]), reverse=True)[0]
            matched_category = longest_matched_keyword[0]
            return matched_category

        return 'Uncategorized'
