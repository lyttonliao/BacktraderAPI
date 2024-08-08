from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime

from .auth_handler import decode_jwt
from ..utils.config import app_settings


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):

        super().__init__(auto_error=auto_error)


    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token")

        user_id = self.get_current_user(credentials.credentials)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

        return user_id
    

    @classmethod
    def get_current_user(self, token: str):
        payload = decode_jwt(token)

        if not payload:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
        
        return payload["sub"]
        

    @classmethod
    def verify_jwt(self, token: str) -> bool:
        payload = decode_jwt(token)

        if payload is None:
            return False
        
        return True