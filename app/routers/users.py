from fastapi import APIRouter, Query, Path, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated

from ..schemas import user as user_schema, strategy as strategy_schema
from ..crud import users as users_crud, strategies as strategies_crud 
from ..dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)
    
@router.post("/", response_model=user_schema.User)
async def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = users_crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    return users_crud.create_user(db, user)

@router.get("/${user_id}", response_model=user_schema.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users_crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/{user_id}/strategies/", response_model=strategy_schema.Strategy)
async def create_strategy_for_user(strategy: strategy_schema.StrategyCreate, db: Session = Depends(get_db)):
    try:
        db_strategy = strategies_crud.create_user_strategy(db, strategy)
        return db_strategy
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="You have already used that name.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users_crud.get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()
    db.refresh(db_user)
    return