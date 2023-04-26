from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Relationship
from backend.validators import Chapters, Positions, Departments, datetime
import bcrypt


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
    tasks: Mapped[List["Task"]] = Relationship("Task", back_populates="owner")

    def set_password(self, password) -> None:
        bytePassword = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
        self.password = bytePassword.decode("utf-8")
        return

    def check_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def __repr__(self):
        return f"User('{self.first_name}','{self.last_name}','{self.username}','{self.email}')"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    department: Mapped[str] = mapped_column(String(30))
    content: Mapped[str] = mapped_column(String(1000))
    attachment: Mapped[Optional[str]] = mapped_column(String(255))
    date_posted: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow())
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped[User] = Relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"Task('{self.id}','{self.title}','{self.content}','{self.attachment}',{self.date_posted}','{self.deadline}','{self.user_id}')"
 
