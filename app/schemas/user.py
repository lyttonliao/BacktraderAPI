from pydantic import BaseModel

from .strategy import Strategy

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    strategies: list[Strategy] = []

    class Config:
        from_attributes = True
