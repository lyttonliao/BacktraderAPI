from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence

from ..models import Strategy as strategy_model
from ..schemas.strategy import Strategy, StrategyUpdate, StrategyCreate
from ..utils.errors import RecordNotFoundError, StatusForbiddenError


async def get_strategies(db: AsyncSession, offset: int = 0, limit: int = 20) -> Sequence[Strategy]:
    results = await db.execute(select(strategy_model.id).limit(limit).offset(offset))
    db_strategies = results.scalars().all()
    return db_strategies


async def get_strategy(db: AsyncSession, strategy_id: int) -> Strategy:
    db_strategy = (
        await db.scalars(select(strategy_model).where(strategy_model.id == strategy_id))
    ).first()

    if db_strategy is None:
        raise RecordNotFoundError
    
    return db_strategy


async def create_user_strategy(db: AsyncSession, params: StrategyCreate) -> Strategy:
    db_strategy = strategy_model(**params.model_dump())
    db.add(db_strategy)
    await db.commit()
    await db.refresh(db_strategy)
    return db_strategy


async def update_user_strategy(db: AsyncSession, params: StrategyUpdate, strategy_id: int, user_id: int) -> Strategy:
    db_strategy = await get_strategy(db, strategy_id)
    
    if not db_strategy:
        raise RecordNotFoundError
    if db_strategy.user_id != user_id:
        raise StatusForbiddenError

    for attr, value in params.model_dump(exclude_unset=True).items():
        setattr(db_strategy, attr, value)
    
    db.add(db_strategy)
    await db.commit()
    await db.refresh(db_strategy)
    return db_strategy


async def delete_strategy(db: AsyncSession, strategy_id: int, user_id: int) -> Strategy:
    db_strategy = await get_strategy(db, strategy_id)

    if not db_strategy:
        raise RecordNotFoundError
    if db_strategy.user_id != user_id:
        raise StatusForbiddenError

    await db.delete(db_strategy)
    await db.commit()
    return db_strategy