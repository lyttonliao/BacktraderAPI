from fastapi import APIRouter, Query, Path, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.schemas.user import User, UserCreate
from app.schemas.strategy import Strategy, StrategyCreate
from app.crud import users, strategies
from app.dependencies import get_db
from app.utils.errors import RecordNotFoundError

router = APIRouter(
    prefix="/users",
    tags=["users"],
)
    
@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    user_params = UserCreate(**user.model_dump())
    db_user = await users.create_user(db, user_params)
    return db_user


@router.get("/${user_id}", response_model=User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await users.get_user_by_id(db, user_id)
    return db_user


@router.post("/{user_id}/strategies/", response_model=Strategy)
async def create_strategy_for_user(strategy: StrategyCreate, db: AsyncSession = Depends(get_db)):
    db_strategy = await strategies.create_user_strategy(db, strategy)
    
    

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = users.get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()
    db.refresh(db_user)
    return