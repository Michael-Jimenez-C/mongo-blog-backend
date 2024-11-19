import os
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError

KEY = os.urandom(32).hex()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

def createToken(data: dict, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=10)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decodeToken(token: str):
    try:
        payload = jwt.decode(token, KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        return None
    except Exception as e:
        print(e)
        return None
