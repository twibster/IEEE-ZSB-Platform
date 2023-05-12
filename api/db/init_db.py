from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.config import configs
from api.db.models import Base
import api.db.listeners

engine = create_engine(configs.DATABASE_URI)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
