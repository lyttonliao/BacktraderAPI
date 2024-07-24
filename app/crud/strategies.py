from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence

from app.models import Strategy as strategy_model
from app.schemas.strategy import Strategy, StrategyUpdate, StrategyCreate
from app.utils.errors import RecordNotFoundError


async def get_strategies(db: AsyncSession, skip: int = 0, limit: int = 20) -> Sequence[Strategy]:
    results = await db.execute(select(strategy_model.id))
    strategies = results.scalars().all()
    return strategies

async def get_strategy(db: AsyncSession, strategy_id: int) -> Strategy:
    strategy = (
        await db.scalars(select(strategy_model).where(strategy_model.id == strategy_id))
    ).first()

    if strategy is None:
        raise RecordNotFoundError
    
    return strategy

async def create_user_strategy(db: AsyncSession, params: StrategyCreate) -> Strategy:
    strategy = strategy_model(**params.model_dump())
    db.add(strategy)
    await db.commit()
    await db.refresh(strategy)
    return strategy

async def update_user_strategy(db: AsyncSession, params: StrategyUpdate, strategy_id: int) -> Strategy:
    strategy = await get_strategy(db, strategy_id)

    for attr, value in params.model_dump(exclude_unset=True).items():
        setattr(strategy, attr, value)
    
    db.add(strategy)
    await db.commit()
    await db.refresh(strategy)
    return strategy

async def delete_strategy(db: AsyncSession, strategy_id: int) -> Strategy:
    strategy = await get_strategy(db, strategy_id)
    await db.delete(strategy)
    await db.commit()
    return strategy