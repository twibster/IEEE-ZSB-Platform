from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config import configs
from backend.database.models import Base

engine = create_engine(configs.DATABASE_URI)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
