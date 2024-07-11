from sqlalchemy.orm import Session

from ..models import strategy as strategy_model
from ..schemas import strategy as strategy_schema

def get_strategies(db: Session, skip: int = 0, limit: int = 20):
    return db.query(strategy_model.Strategy).offset(skip).limit(limit).all()

def get_strategy(db: Session, strategy_id: int):
    return db.query(strategy_model.Strategy).filter(strategy_model.Strategy.id == strategy_id).first()

def create_user_strategy(db: Session, strategy: strategy_schema.StrategyCreate, user_id: int):
    db_strategy = strategy_model.Strategy(**strategy.model_dump(), user_id=user_id)
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy
