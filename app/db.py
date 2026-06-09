from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import String, ForeignKey
from flask_login import UserMixin

from app.md_engine import engine


class Base(DeclarativeBase):
    pass


class User(Base, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    diaries: Mapped[list["Diary"]] = relationship(
        "Diary",
        back_populates="user"
    )


class Diary(Base):
    __tablename__ = "diaries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str | None] = mapped_column(String(60), nullable=False)
    content: Mapped[str | None] = mapped_column(nullable=True)
    user: Mapped["User"] = relationship(
        "User",
        back_populates="diaries"
    )


Base.metadata.create_all(engine)