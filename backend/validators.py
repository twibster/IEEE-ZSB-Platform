from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, constr


class Positions(str, Enum):
    CHAIRMAN = "chairman"
    LEADER = "leader"
    MEMBER = "member"
    ROOKIE = "rookie"


class Chapters(str, Enum):
    RAS, PES, CS = "ras", "pes", "cs"


class Departments(str, Enum):
    ES = "embedded systems"
    AI = "ai"
    ROS = "ros"
    MECHANICAL = "mechanical"
    MOBILE = "mobile"
    WEB = "web"
    POWER = "power"
    DISTRIBUTION = "distribution"


class UserValidator(BaseModel):
    """A Pydantic data model for validating user input.

    Attributes:
        first_name (str): The user's first name. Must be between 2 and 20 characters.
        last_name (str): The user's last name. Must be between 2 and 20 characters.
        birthdate (datetime): The user's birthdate.
        email (EmailStr): The user's email address.
        username (str): The user's desired username. Must be between 3 and 16 characters and only contain alphanumeric characters, hyphens, and underscores.
        password (str): The user's desired password. Must be at least 8 characters long.
        chapter (Optional[Chapters]): The user's chapter, if applicable.
        department (Optional[Departments]): The user's department, if applicable.
        position (Positions): The user's position within the organization.
    """
    first_name: str = Field(min_length=2, max_length=20)
    last_name: str = Field(min_length=2, max_length=20)
    birthdate: datetime
    email: EmailStr
    username: constr(regex=r'^[a-zA-Z0-9_-]{3,16}$')  # type: ignore
    password: str = Field(min_length=8)
    chapter: Optional[Chapters]
    department: Optional[Departments]
    position: Positions

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Jacky",
                "birthdate": "2023-04-24T22:01:32.904Z",
                "email": "user@example.com",
                "username": "j3uvaobz",
                "password": "stringst",
                "chapter": "ras",
                "department": "embedded systems",
                "position": "leader"
            }
        }


class LoginValidator(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "jsxht",
                "password": "string"
            }
        }


class TaskValidator(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    department: Departments
    content: str = Field(max_length=1000)
    attachment: str
    date_created: datetime
    deadline: datetime

    class Config:
        schema_extra = {
            "example": {
                "title": "First task in AI",
                "department": "ai",
                "content": "look at the attached file",
                "attachment": "I am an attached file dude",
                "date_created": "2023-04-25T19:52:28.327Z",
                "deadline": "2023-06-25T19:52:28.327Z"
                }
        }
