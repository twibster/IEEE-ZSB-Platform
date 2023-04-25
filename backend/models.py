import bcrypt as bc
from typing import Optional
from backend.validators import  Chapters, Positions, Departments, datetime

class User:
    id: Optional[int]
    first_name: str 
    last_name: str
    birthdate: datetime
    email: str
    username: str
    password: str 
    chapter: Optional[Chapters]
    department: Optional[Departments]
    position: Positions

    def set_password(self, password) -> None:
        hashed_pass = bc.hashpw(password.encode("utf-8"),bc.gensalt())
        self.password = hashed_pass.decode("utf-8")
        return
    
    def check_password(self, password) -> bool:
        return bc.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
    
    def __init__(self, id, first_name, last_name, birthdate,email, username, chapter, department, position, password=None) -> None:
        self.id= id
        self.first_name= first_name
        self.last_name= last_name
        self.birthdate= birthdate
        self.email= email
        self.username= username
        self.chapter= chapter
        self.department= department
        self.position= position
        return