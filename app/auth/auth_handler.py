import time
import jwt
from typing import Dict, Annotated
from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.ext.asyncio import AsyncSession


from app.schemas.user import User
from app.crud.users import get_user_by_id
from app.utils.errors import InvalidTokenError
from app.utils.config import app_settings
from app.schemas.token import TokenData
from app.crud.users import get_user_by_email


oauth2_scheme = OAuth2AuthorizationCodeBearer(t)


async def authenticate_user(db: AsyncSession, user_id: int) -> User:
    user = await get_user_by_id(db, user_id)

    if user is None:
        return False
    
    return user


async def get_current_user(db: AsyncSession, token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, app_settings.secret_key, algorithms=[app_settings.algorithm])
    email = payload.get("sub")

    if email is None:
        raise InvalidTokenError
    
    token_data = TokenData(email=email)
    user = await get_user_by_email(db, email=token_data.email)

    if user is None:
        raise InvalidTokenError
    
    return user