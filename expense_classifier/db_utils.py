import pandas as pd

from database import select, DatabaseHandler
from models import Category

db_handler = DatabaseHandler()

default_categories = {
    "Housing & Utilities": ['rent', 'swaroop'],
    "Shopping": ['amazon', 'myntra', 'reliance', 'ajio', 'decathlon', 'croma', 'vouchagram', 'bata', 'centro'],
    "Groceries": ['swiggy.sto', 'swiggyinstamart', 'swiggy.instamart', 'swiggystores', 'swiggy.stores', 'zepto',
                  'geddit', 'blinkit', 'grofers'],
    "Food & Drinks": ['swiggy', 'swiggyupi', 'swiggyfood'],
    "Vehicle": ['petrol', 'fuel'],
    "Health & Personal Development": [],
    "Transportation": ['uber', 'uberrides', 'bmtc', 'ola', 'olacabs', 'metro'],
    "Life & Entertainment": [],
    "Internet & OTT bills": [],
    "Savings & Investments": ['bsestarmfrzp', 'groww', 'ipo.'],
    "Financial Expenses": [],
    "Gifts & Transfers": [],
    "Splitwise & Lendings": ['divyanshi', 'ankur', 'aksht', 'aksht jain', 'anvesha'],
    "Flights Tickets": [],
    "Self Transfer": ['8765830338@', 'piyush upreti'],
    "General": [],
    "Unknown": []
}


def get_category_keywords() -> dict:

    df = pd.read_sql(select(Category), db_handler.engine)
    mapping = {}
    for item in df.iterrows():
        row = item[1].to_dict()
        mapping[row.get('name')] = row.get('keywords')
    return mapping


def add_keyword(category, kw_column, kw_value):
    pass


def update_keywords(category_mapping: dict[str, set]):

    with db_handler.SessionLocal() as session:
        for category, new_keywords in category_mapping.items():
            record = session.query(Category).filter_by(name=category).first()
            if record:
                existing_keywords = set(record.keywords or [])
                updated_keywords = list(existing_keywords | new_keywords)
                record.keywords = updated_keywords
        session.commit()
    print("Keywords updated successfully.")






