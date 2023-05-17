import bcrypt
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Relationship
from api.const import Chapters, Positions, Departments


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    birthdate: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(255)) 
    chapter: Mapped[Optional[Chapters]] = mapped_column(String(30))
    department: Mapped[Optional[Departments]] = mapped_column(String(30))
    position: Mapped[Positions] = mapped_column(String(30))
    tasks: Mapped[List["Task"]] = Relationship("Task", back_populates="owner", cascade="all, delete", lazy="dynamic")
    meetings: Mapped[List["Meeting"]] = Relationship("Meeting", back_populates="owner", cascade="all, delete")
    permissions: Mapped["Permission"] = Relationship("Permission", back_populates="user", cascade="all, delete")

    def set_password(self, password: str) -> None:
        bytePassword = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.password = bytePassword.decode("utf-8")
        return 

    def check_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
    
    def update(self, first_name: str, last_name: str, birthdate: datetime, email: str, username: str, password: str, chapter: Optional[Chapters], department: Optional[Departments], position: Positions, **kwargs) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.email = email
        self.username = username
        self.set_password(password)
        self.chapter = chapter
        self.department = department
        self.position = position

    def __repr__(self):
        return f"User('{self.first_name}','{self.last_name}','{self.username}','{self.email}')"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    department: Mapped[str] = mapped_column(String(30))
    content: Mapped[str] = mapped_column(String(1000))
    attachment: Mapped[Optional[str]] = mapped_column(String(255))
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow())
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped[User] = Relationship(back_populates="tasks")

    def update(self, title: str, department: str, content: str, deadline: datetime, attachment: Optional[str] = None, **kwargs) -> None:
        self.title = title
        self.department = department
        self.content = content
        self.attachment = attachment
        self.deadline = deadline

    def __repr__(self):
        return f"Task('{self.id}','{self.title}','{self.content}','{self.attachment}',{self.date_created}','{self.deadline}')"


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    view_task: Mapped[bool] = mapped_column(default=False)
    create_task: Mapped[bool] = mapped_column(default=False)
    modify_task: Mapped[bool] = mapped_column(default=False)
    delete_task: Mapped[bool] = mapped_column(default=False)
    submit_task: Mapped[bool] = mapped_column(default=False)
    excuse_task: Mapped[bool] = mapped_column(default=False) 
    view_user: Mapped[bool] = mapped_column(default=False)
    confirm_user: Mapped[bool] = mapped_column(default=False)
    modify_user: Mapped[bool] = mapped_column(default=False)
    delete_user: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = Relationship(back_populates="permissions")

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"MyClass({attrs})"


class Meeting(Base):
    __tablename__ = "meetings"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    details: Mapped[str] = mapped_column(String(1000))
    type: Mapped[str] = mapped_column(String(7))
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    location: Mapped[Optional[str]] = mapped_column(String(2000))
    url: Mapped[Optional[str]] = mapped_column(String(255))
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=datetime.utcnow())
    chapter: Mapped[Optional[Chapters]]
    department: Mapped[Optional[Departments]]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped[User] = Relationship(back_populates="meetings")

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"MyClass({attrs})"

