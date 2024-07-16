from pydantic import BaseModel

class StrategyBase(BaseModel):
    name: str
    public: bool
    tags: list[str] = []

class StrategyCreate(StrategyBase):
    pass

class Strategy(StrategyBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
