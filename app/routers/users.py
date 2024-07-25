from fastapi import APIRouter, Query, Path, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from ..schemas.user import User, UserCreate
from ..schemas.strategy import Strategy, StrategyCreate, StrategyUpdate
from ..crud import users, strategies
from ..database.session import get_db
from ..utils.errors import StatusForbiddenError
from ..auth.auth_bearer import JWTBearer
from ..auth.auth_handler import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)
    
@router.post("/", response_model=User, dependencies=[Depends(JWTBearer())])
async def create_user(
    user: UserCreate, 
    db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    user_params = UserCreate(**user.model_dump())
    db_user = await users.create_user(db, user_params)
    return db_user


@router.get("/${user_id}", response_model=User, dependencies=[Depends(JWTBearer())])
async def read_user(
    user_id: int, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_user = await users.get_user_by_id(db, user_id)
    return db_user


@router.post("/{user_id}/strategies", response_model=Strategy, dependencies=[Depends(JWTBearer())])
async def create_strategy_for_user(
    strategy: StrategyCreate, 
    db: Annotated[AsyncSession, Depends(get_db)], 
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    if user_id != current_user.id:
        raise StatusForbiddenError
    
    strategy_params = StrategyCreate(**strategy.model_dump(), user_id=current_user.id)
    db_strategy = await strategies.create_user_strategy(db, strategy_params)
    return db_strategy


@router.patch("/{user_id}/strategies/{strategy_id}", response_model=Strategy, dependencies=[Depends(JWTBearer())])
async def update_strategy_for_user(
    strategy: StrategyUpdate,
    db: Annotated[AsyncSession, Depends(get_db)], 
    user_id: int,
    strategy_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    if user_id != current_user.id:
        raise StatusForbiddenError
    
    strategy_params = StrategyUpdate(**strategy.model_dump(exclude_unset=True))
    db_strategy = await strategies.update_user_strategy(db, strategy_params, strategy_id)
    return db_strategy

    

@router.delete("/{user_id}", response_model=User, dependencies=[Depends(JWTBearer())])
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = users.get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
