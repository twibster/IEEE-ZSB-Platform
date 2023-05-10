import string
import random
from backend import engine
from sqlalchemy.orm import sessionmaker


def generate_random_string(length: int, email: bool = False) -> str:
    alpha = list(string.ascii_lowercase)
    generated_string = ""
    for _ in range(length):
        generated_string += alpha[random.randint(0, len(alpha)-1)]
    return generated_string+"@default.com" if email else generated_string


def drop_database_tables(Base) -> None:
    # Get the metadata object associated with the session's bind
    metadata = Base.metadata

    # Drop all tables
    metadata.drop_all(bind=engine)


def create_database_tables(Base,engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    return db
