from fastapi import Header, HTTPException
from typing import Annotated

from .database import SessionLocal


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    
async def get_query_token(token: str):
    if token != "random_token":
        raise HTTPException(status_code=400, detail="No random_token provided")
    
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()