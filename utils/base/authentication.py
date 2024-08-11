import uuid
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from api.users.model import Users
from utils.base.config import settings
from utils.base.session import AsyncDatabase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login", scheme_name="JWT")
KEY = settings.mick.salt
ALGORITHM = "HS256"


async def create_access_token(data: dict, expires_delta: timedelta = None):
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(hours=4)
    encoding = data | {"exp": expire}
    encoded_jwt = jwt.encode(encoding, KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_refresh_token(data: dict, expires_delta: timedelta = None):
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(days=3)
    encoding = data | {"exp": expire}
    encoded_jwt = jwt.encode(encoding, KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_token(token: str):
    try:
        decode_jwt = jwt.decode(token=token, key=KEY, algorithms=[ALGORITHM])
        return decode_jwt
    except ExpiredSignatureError:
        raise HTTPException(401, detail="Token expired")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token: " + str(e))


async def encode_token(data: dict):
    encoded_jwt = jwt.encode(data, KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_me(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")
    try:
        payload = jwt.decode(token=token, key=KEY, algorithms=[ALGORITHM])

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token: " + str(e))

    if payload.get("exp") and payload["exp"] < datetime.timestamp(datetime.utcnow()):
        raise HTTPException(status_code=401, detail="Token expired")

    session = await AsyncDatabase.return_session()
    try:
        query = await session.scalars(select(Users).where(Users.id == payload.get('user_id')))
        user = query.first()
        if user.active is False:
            raise HTTPException(status_code=401, detail="User deactivate")
        return user
    finally:
        await session.close()
