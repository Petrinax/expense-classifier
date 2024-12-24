from sqlalchemy import Column, Integer, String, Text, JSON, ARRAY, DateTime, Numeric, DATE, Date, TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'categories'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, primary_key=True)
    keywords = Column(ARRAY(String), nullable=True)
    desc = Column(String, nullable=True)


class RawTransaction(Base):
    __tablename__ = 'raw_transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    amount = Column(Numeric(38, 9), nullable=False)
    narration = Column(Text, nullable=False)
    bank_account = Column(String, nullable=True)


def validate_model(f):
    def wrapper(self, model, *args, **kwargs):
        if model not in Base.__subclasses__():
            raise TypeError(f"Invalid Model provided. Available models: {Base.__subclasses__()}")
        return f(self, model, *args, **kwargs)
    return wrapper


