from datetime import date
from pydantic import BaseModel
from typing import Optional


# Схема для створення контакту
class ContactCreateModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date

# Схема для оновлення контакту
class ContactUpdateModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None

# Схема для відображення контакту
class ContactModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date