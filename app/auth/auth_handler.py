import time
import jwt
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession


from ..schemas.user import User
from ..utils.errors import InvalidTokenError, ExpiredTokenError
from ..utils.config import app_settings
from ..schemas.token import TokenData
from ..crud.users import get_user_by_email
from ..database.session import get_db


with open("C:/Users/xlord/.ssh/id_rsa", "r") as f:
    SECRET_KEY = f.read()


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[app_settings.algorithm])
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError
    except jwt.InvalidTokenError:
        raise InvalidTokenError
    
    return payload


async def get_current_user(
    token: str,
    db: Annotated[AsyncSession, Depends(get_db)], 
):
    payload = decode_jwt(token)
    email = payload.get("sub")

    if email is None:
        raise InvalidTokenError
    
    token_data = TokenData(email=email)
    user = await get_user_by_email(db, email=token_data.email)

    if user is None:
        raise InvalidTokenError
    
    return user
