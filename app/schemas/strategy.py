from pydantic import BaseModel, ConfigDict
from typing import Optional

class StrategyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    public: bool
    tags: Optional[list[str]] = []

class StrategyCreate(StrategyBase):
    user_id: int

class StrategyUpdate(StrategyBase):
    pass

class Strategy(StrategyBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
