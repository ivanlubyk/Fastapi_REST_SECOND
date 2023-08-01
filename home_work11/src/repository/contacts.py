from datetime import date, timedelta
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models import Contact
from src.schemas import ContactCreateModel, ContactUpdateModel, ContactModel
from sqlalchemy import extract

async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    sq = select(Contact).offset(offset).limit(limit)
    result = await db.execute(sq)
    contacts = result.scalars().all()
    return contacts



async def get_contact(contact_id: int, db: AsyncSession) -> Optional[ContactModel]:
    contact = await db.execute(select(Contact).filter(Contact.id == contact_id))
    db_contact = contact.scalar()
    if not db_contact:
        return None
    return ContactModel(
        id=db_contact.id,
        first_name=db_contact.first_name,
        last_name=db_contact.last_name,
        email=db_contact.email,
        phone=db_contact.phone,
        birthday=db_contact.birthday,
    )


async def put_contact(contact_id, contact_update: ContactUpdateModel, db: AsyncSession):


    db_contact = await db.execute(select(Contact).filter(Contact.id == contact_id))
    contact = db_contact.scalar()
    if contact_update.get("first_name") is not None:
        contact.first_name = contact_update.get("first_name")
    if contact_update.get("last_name") is not None:
        contact.last_name = contact_update.get("last_name")
    if contact_update.get("email") is not None:
        contact.email = contact_update.get("email")
    if contact_update.get("phone") is not None:
        contact.phone = contact_update.get("phone")
    if contact_update.get("birthday") is not None:
        contact.phone = str(contact_update.get("birthday"))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def del_contact(contact_id: int, db: AsyncSession) -> Optional[ContactModel]:
    async with db.begin():
        contact = await db.execute(select(Contact).filter(Contact.id == contact_id))
        db_contact = contact.scalar()
        if not db_contact:
            return None

        db.delete(db_contact)
        await db.commit()

        return ContactModel(
            id=db_contact.id,
            first_name=db_contact.first_name,
            last_name=db_contact.last_name,
            email=db_contact.email,
            phone=db_contact.phone,
            birthday=db_contact.birthday,
        )


async def search(first_name: str, last_name: str, email: str, db: AsyncSession) -> List[ContactModel]:
    async with db.begin():
        query = select(Contact).filter(
            (Contact.first_name.ilike(f'%{first_name}%')) |
            (Contact.last_name.ilike(f'%{last_name}%')) |
            (Contact.email.ilike(f'%{email}%'))
        )
        contacts = await db.execute(query)
        return [ContactModel(
            id=contact.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            phone=contact.phone,
            birthday=contact.birthday,
        ) for contact in contacts.scalars()]





async def upcoming_birthdays(db: AsyncSession) -> List[Contact]:
    today = date.today()
    next_week = today + timedelta(days=7)
    async with db.begin():
        statement = select(Contact).filter(
            (extract('month', Contact.birthday) == today.month) &
            (extract('day', Contact.birthday) >= today.day) &
            (extract('day', Contact.birthday) <= next_week.day)
        )
        contacts = await db.execute(statement)
        return contacts.scalars().all()
