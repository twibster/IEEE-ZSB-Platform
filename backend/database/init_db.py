from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base

engine = create_engine("sqlite:///platform.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db = Session()