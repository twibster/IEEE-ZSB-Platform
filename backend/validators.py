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


class userValidator(BaseModel):
    id: Optional[int] = Field(gt=0)
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
                "id": 1,
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


class loginValidator(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "jsxht",
                "password": "string"
            }
        }
