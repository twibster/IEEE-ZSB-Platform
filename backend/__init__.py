from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base

engine = create_engine("sqlite:///platform.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db = Session()

permissions = {
    "chairman": ['view-task', 'create-task', 'delete-user', 'confirm-user', 'view-user','delete-task'],
    "leader": ['view-task', 'create-task', 'delete-task'],
    "member": ['view-task', 'submit-task', 'excuse-task'],
    "rookie": ['view-task', 'submit-task', 'excuse-task']
}