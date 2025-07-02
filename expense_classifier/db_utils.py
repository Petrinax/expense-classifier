import pandas as pd

from expense_classifier.database import select, DatabaseHandler
from expense_classifier.models import Category

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
    "Unknown": [],


    'Salary': ['wm global tech'],
    'Cashback & Refunds': ['ONE97', 'One Ninety Seven'],
    'Interest on Savings': ['credit interest', 'int.pd'],
    'Interest on Deposits': ['io for'],
    'Interest on Investments': [],
    'Interest on Other Accounts': [],
    'Dividends': ['npci', 'nach'],
    'Savings and Investments': [],
    'Capital Gains': [],
}

income_categories = {


}
# Sample desc for LLM prompts
category_descriptions = [
    "Transactions for rent, housing, or utilities like electricity or water bills. Keywords: rent, swaroop",
    "Shopping-related transactions including online or retail stores. Keywords: amazon, myntra, reliance, ajio, decathlon, croma, vouchagram, bata, centro",
    "Grocery purchases or quick commerce platforms. Keywords: swiggy.sto, swiggyinstamart, swiggy.instamart, swiggystores, swiggy.stores, zepto, geddit, blinkit, grofers",
    "Spending on food delivery or restaurants. Keywords: swiggy, swiggyupi, swiggyfood",
    "Fuel or petrol-related vehicle expenses. Keywords: petrol, fuel",
    "Health, fitness, or personal development spending. Keywords: [empty]",
    "Transportation services like ride sharing or public transport. Keywords: uber, uberrides, bmtc, ola, olacabs, metro",
    "Entertainment or leisure expenses. Keywords: [empty]",
    "Internet, mobile, or OTT subscription bills. Keywords: [empty]",
    "Investment or savings-related transactions. Keywords: bsestarmfrzp, groww, ipo.",
    "Bank charges, interest, or other financial fees. Keywords: [empty]",
    "Gifts or money transfers to friends/family. Keywords: [empty]",
    "Splitwise settlements or money lent/borrowed. Keywords: divyanshi, ankur, aksht, aksht jain, anvesha",
    "Flight or airline ticket bookings. Keywords: [empty]",
    "Transfers between own accounts or self. Keywords: 8765830338@, piyush upreti",
    "General expenses that don't fit other categories. Keywords: [empty]",
    "Unknown or uncategorized transactions. Keywords: [empty]"
]


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






