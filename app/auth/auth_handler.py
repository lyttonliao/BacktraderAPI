import jwt

from ..utils.errors import InvalidTokenError, ExpiredTokenError
from ..utils.config import app_settings


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
