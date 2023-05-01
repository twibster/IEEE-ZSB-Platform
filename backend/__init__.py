from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base

engine = create_engine("sqlite:///platform.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db = Session()

permissions = {
    "chairman": ['view-task', 'create-task', 'modify-task', 'delete-task', 'view-user', 'confirm-user', 'modify-user', 'delete-user'],
    "leader": ['view-task', 'create-task', 'modify-task', 'delete-task', 'modify-user'],
    "member": ['view-task', 'submit-task', 'excuse-task', 'modify-user'],
    "rookie": ['view-task', 'submit-task', 'excuse-task', 'modify-user']
}