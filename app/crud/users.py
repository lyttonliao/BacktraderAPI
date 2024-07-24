from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models import User as user_model
from ..schemas.user import User, UserCreate
from ..utils.errors import RecordNotFoundError


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    user = (
        await db.scalars(select(user_model).where(user_model.email == email))
    ).first()

    if user is None:
        raise RecordNotFoundError
    
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    user = (
        await db.scalars(select(user_model).where(user_model.id == user_id))
    ).first()
    
    if user is None:
        raise RecordNotFoundError
    
    return user


async def create_user(db: AsyncSession, params: UserCreate) -> User:
    user = user_model(name=params.name, email=params.email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> User:
    user = get_user_by_id(db, user_id)
    db.delete(user)
    await db.commit()
    return user