import jwt
import rsa

from ..utils.errors import InvalidTokenError, ExpiredTokenError
from ..utils.config import app_settings


def private_key():
    with open("C:/Users/xlord/.ssh/id_rsa.pub", mode="rb") as f:
        key_data = f.read()
        key = rsa.PublicKey._load_pkcs1_pem(key_data)

    return key


def decode_jwt(token: str):
    key = private_key()

    try:
        payload = jwt.decode(token, key, algorithms=[app_settings.algorithm])
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError
    except jwt.InvalidTokenError:
        raise InvalidTokenError
    
    return payload
