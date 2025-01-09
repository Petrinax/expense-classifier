from functools import wraps
from sqlalchemy import create_engine, insert, select, inspect
from sqlalchemy.orm import sessionmaker

from expense_classifier.common_utils import get_file_content
from models import Base, Category, validate_model


class DatabaseHandler:
    def __init__(self, db_url: str = get_file_content('/Users/piyushupreti/Documents/Projects/expense-classifier'
                                                      '/local_files/sql_alchemy_url.txt')):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @validate_model
    def insert_data(self, model: type(Base), data):
        with self.SessionLocal() as session:
            session.execute(insert(model), data)
            session.commit()

    @validate_model
    def get_data(self, model: type(Base)):
        if model not in Base.__subclasses__():
            print("Invalid Model provided.")
            print(f"Available models: {Base.__subclasses__()}")
        # inspector = inspect(self.engine)
        # columns = [column['name'] for column in inspector.get_columns(model.__tablename__)]
        with self.SessionLocal() as session:
            result = session.query(select(model))
        return result.all()



# Example Usage
if __name__ == '__main__':
    db_handler = DatabaseHandler()

    # from classifier import Classifier
    # categories = Classifier().category_keywords
    #
    # categories = [{"name": name, "keywords": keywords} for name, keywords in categories.items()]
    #
    # db_handler.insert_data(Category, categories)
    # db_categories = db_handler.get_data(Category)
