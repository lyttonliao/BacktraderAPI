from fastapi import APIRouter
from pydantic import BaseModel
from typing import Annotated

class Strategy(BaseModel):
    id: int
    name: str
    public: bool
    fields: list[str]
    criteria: list[str]
    userID: int
    version: int

router = APIRouter(
    prefix="/strategies",
    tags=["strategies"],
    responses={404: {"description": "Not Found"}}
)

fake_strats_db = {"strategy1": {"name", }}

@router.post("/")
async def create_strategy(strategy: Strategy):
    return

@router.get("/", response_model=list[Strategy])
async def read_all_strategies():
    return

@router.get("/{strategy_id}")
async def read_strategy():
    return {"strategy": "strategy"}

@router.put(
    "/{strategy_id}",
    responses={403: {"description": "Operation forbidden"}}
)
async def update_strategy(strategy_id: str, strategy: Strategy):
    return {"strategy_id": strategy_id, **strategy.model_dump()}