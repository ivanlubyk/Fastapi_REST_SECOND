from sqlalchemy import Column, Integer, String, DateTime, func, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from src.database.db import Base


class Contact(Base):
    __tablename__ = "contacts" # noqa
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = Column(String, index=True)
    last_name: Mapped[str] = Column(String, index=True)
    email: Mapped[str] = Column(String, unique=True, index=True)
    phone: Mapped[str] = Column(String)
    birthday: Mapped[str] = Column(Date)
    created_at: Mapped[int] = Column(DateTime, default=func.now())

