from fastapi import APIRouter, Query, Path
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

@router.post("/")
async def create_strategy(strategy: Strategy):
    return

@router.get("/", response_model=list[Strategy])
async def read_strategies(
    q: Annotated[
        str | None,
        Query(
            alias="search",
            title="Query strategy name",
            description="Query string to search for relative matches in the database"
        )
    ]
):
    return

@router.get("/{strategy_id}")
async def read_strategy(
    strategy_id: Annotated[int, Path(title="The ID of the strategy")]
):
    return {"strategy": strategy_id}

@router.put(
    "/{strategy_id}",
    responses={403: {"description": "Operation forbidden"}}
)
async def update_strategy(strategy_id: str, strategy: Strategy):
    return {"strategy_id": strategy_id, **strategy.model_dump()}