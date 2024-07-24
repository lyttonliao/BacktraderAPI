from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decode_jwt

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
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code")
        return credentials.credentials
    
    def verify_jwt(self, token: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_jwt(token)
            
            if payload:
                isTokenValid = True
        except:
            payload = None

        return isTokenValid
