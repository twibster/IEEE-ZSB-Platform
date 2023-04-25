import bcrypt
from typing import Optional
from backend.validators import  Chapters, Positions, Departments, datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    birthdate: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(255)) 
    chapter: Mapped[Optional[Chapters]] = mapped_column(String(30))
    department: Mapped[Optional[Departments]] =mapped_column(String(30))
    position: Mapped[Positions] =mapped_column(String(30))

    def set_password(self, password) -> None:
        bytePassword = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
        self.password = bytePassword.decode("utf-8")
        return
    
    def check_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))