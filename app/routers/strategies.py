from fastapi import APIRouter, Query, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from ..schemas import strategy as schema
from ..database.session import get_db
from ..crud import strategies as crud
from ..auth.auth_bearer import JWTBearer


router = APIRouter(
    prefix="/strategies",
    tags=["strategies"],
)


@router.get("/{strategy_id}", response_model=schema.Strategy, dependencies=[Depends(JWTBearer())])
async def read_strategy(strategy_id: int, db: AsyncSession = Depends(get_db)):
    db_strategy = crud.get_strategy(db, strategy_id)
    return db_strategy


@router.get("/", response_model=list[schema.Strategy], dependencies=[Depends(JWTBearer())])
async def read_strategies(db: AsyncSession = Depends(get_db)):
    return crud.get_strategies(db)
