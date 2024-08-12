from pydantic import BaseModel, ConfigDict
from typing import Optional

class StrategyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    public: Optional[bool] = False
    tags: Optional[list[str]] = []

class StrategyCreate(StrategyBase):
    user_id: Optional[int] = None

class StrategyUpdate(StrategyBase):
    pass

class Strategy(StrategyBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
