import jwt
import secrets
from fastapi import HTTPException, Query
from .db_handler import *
from .models import *
from .cache_handler import *
from .keys import (private_key, public_key)
from passlib.context import CryptContext
import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_pwd_hash(password: str) -> str:
    return pwd_context.hash(password)


async def verify_password(username: str, password: str):
    creds = await get_user_creds(username)
    if not creds:
        raise HTTPException(status_code=404, detail="User not found")
    return (pwd_context.verify(password, creds["password"]), creds['_id'])


async def add_user(username: str, password: str) -> None:
    try:
        exists = await get_user_creds(username)
        if exists:
            raise HTTPException(
                status_code=422, detail="Username already exists")
        await set_user_creds(username, get_pwd_hash(password))
        return {"message": "User added successfully"}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


async def generate_tokens(expiry_time: int, _id: str, refresh: str = None) -> str:
    expiration_time = datetime.datetime.now(datetime.UTC
                                            ) + datetime.timedelta(seconds=expiry_time)
    payload = {
        "id": _id,
        "expiration": expiration_time.isoformat()
    }
    encoded_access = jwt.encode(payload, private_key, algorithm="RS256")
    if refresh:
        return {"access_token": encoded_access, "refresh token": refresh}
    csrf_token = secrets.token_urlsafe(32)
    refresh_expiration_time = datetime.datetime.now(datetime.UTC
                                                    ) + datetime.timedelta(seconds=3600)
    refresh_payload = {
        'id': _id,
        'csrf_token': csrf_token,
        'expiration': refresh_expiration_time.isoformat()
    }
    add_to_cache(_id, csrf_token)
    encoded_refresh = jwt.encode(
        refresh_payload, private_key, algorithm="RS256")
    return {"access_token": encoded_access, "refresh token": encoded_refresh}


async def refresh_token(token: str):
    try:
        payload = jwt.decode(token, public_key, algorithms=['RS256'])
    except:
        raise HTTPException(status_code=401, detail='Invalid token')
    csrf_token = get_from_cache(payload["id"])
    if not csrf_token:
        raise HTTPException(status_code=401, detail="Invalid CSRF Token")
    else:
        if payload['csrf_token'] == csrf_token:
            gen_token = await generate_tokens(30, payload["id"], token)
        else:
            raise HTTPException(status_code=401, detail="Invalid CSRF Token")

    return gen_token
