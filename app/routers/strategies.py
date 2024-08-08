from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from typing import Annotated

from ..schemas.strategy import Strategy, StrategyCreate, StrategyUpdate
from ..database.session import get_db
from ..crud import strategies
from ..auth.auth_bearer import JWTBearer


router = APIRouter(
    prefix="/v1/strategies",
    tags=["strategies"],
)


@router.post("/", response_model=Strategy, dependencies=[Depends(JWTBearer())])
async def create_strategy_for_user(
    strategy: StrategyCreate, 
    db: Annotated[AsyncSession, Depends(get_db)], 
    user_id: Annotated[str, Depends(JWTBearer())]
):   
    strategy_params = StrategyCreate(**strategy.model_dump())
    strategy_params.user_id = user_id
    db_strategy = await strategies.create_user_strategy(db, strategy_params)
    return db_strategy


@router.get("/{strategy_id}", response_model=Strategy, dependencies=[Depends(JWTBearer())])
async def read_strategy(
    strategy_id: int, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_strategy = await strategies.get_strategy(db, strategy_id)
    return db_strategy


@router.get("/", response_model=list[Strategy], dependencies=[Depends(JWTBearer())])
async def read_strategies(db: Annotated[AsyncSession, Depends(get_db)]):
    db_strategies = await strategies.get_strategies(db)
    return db_strategies


@router.patch("/{strategy_id}", response_model=Strategy)
async def update_strategy_for_user(
    strategy: StrategyUpdate,
    db: Annotated[AsyncSession, Depends(get_db)], 
    strategy_id: int,
    user_id: Annotated[str, Depends(JWTBearer())]
):
    strategy_params = StrategyUpdate(**strategy.model_dump(exclude_unset=True))
    db_strategy = await strategies.update_user_strategy(db, strategy_params, strategy_id, user_id)
    return db_strategy


@router.delete("/{strategy_id}", response_model=Strategy)
async def delete_strategy_for_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    strategy_id: int,
    user_id: Annotated[str, Depends(JWTBearer())]
):
    db_strategy = await strategies.delete_strategy(db, strategy_id, user_id)
    return db_strategy