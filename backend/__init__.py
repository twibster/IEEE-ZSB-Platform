from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, Position

engine = create_engine("sqlite:///platform.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db = Session()

if not db.query(Position).first():
    db.add_all([
        Position(position="chairman", permissions=["view-task", "edit-task", "delete-task", "delete-user"]),
        Position(position="leader", permissions=["view-task", "edit-task", "delete-task"]),
        Position(position="member", permissions=["view-task", "submit-task"]),
        Position(position="rookie", permissions=["view-task", "submit-task"])]
    )
    db.commit()
