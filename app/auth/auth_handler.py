import jwt

from ..utils.errors import InvalidTokenError, ExpiredTokenError


def get_key():
    with open("C:/Users/xlord/.ssh/id_ecdsa.pub", mode="r") as f:
        key_data = f.read()

    return key_data


def decode_jwt(token: str):
    key = get_key()

    try:
        payload = jwt.decode(
            token, 
            key, 
            algorithms=["ES256"],
            audience="BacktestingApi",
            issuer="StratCheck",
        )

    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError
    except jwt.InvalidTokenError:
        raise InvalidTokenError
    
    return payload
