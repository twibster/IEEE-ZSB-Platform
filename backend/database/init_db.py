from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config import Config
from backend.database.models import Base

engine = create_engine(Config.DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db = Session()