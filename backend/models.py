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

    def __init__(self, id, first_name, last_name, birthdate,email, username, password, chapter,department,position) -> None:
        self.id= last_name
        self.first_name= first_name
        self.last_name= last_name
        self.birthdate= birthdate
        self.email= email
        self.username= username
        self.password= password
        self.chapter= chapter
        self.department= department
        self.position= position
    pass