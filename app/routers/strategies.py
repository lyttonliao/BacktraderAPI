from fastapi import APIRouter, Query, Path, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from ..schemas import strategy as schema
from ..dependencies import get_db
from ..crud import strategies as crud


router = APIRouter(
    prefix="/strategies",
    tags=["strategies"],
)


@router.get("/{strategy_id}", response_model=schema.Strategy)
async def read_strategy(strategy_id: int, db: Session = Depends(get_db)):
    db_strategy = crud.get_strategy(db, strategy_id)
    return db_strategy

@router.get("/", response_model=list[schema.Strategy])
async def read_strategies(db: Session = Depends(get_db)):
    return crud.get_strategies(db)
