from pydantic import BaseModel, EmailStr

from .strategy import Strategy

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    strategies: list[Strategy] = []

    class Config:
        from_attributes = True
