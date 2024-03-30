from cachetools import TTLCache
import time
from fastapi.exceptions import HTTPException
from fastapi import status


csrf_cache = TTLCache(maxsize=100, ttl=3600)
otp_cache=TTLCache(maxsize=100,ttl=60)

def add_to_cache(_id: str, token: str):
    csrf_cache[_id] = token


def get_from_cache(_id: str):
    return csrf_cache[_id]

def add_to_otp_cache(email, otp):
    if email in otp_cache:
        timestamp, _ = otp_cache.get(email)
        current_time = time.time()
        if current_time - timestamp < 30:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail='Wait for 30 seconds before requesting another OTP')
    otp_cache[email] = (time.time(), otp)
    return True

def get_from_otp_cache(email):
    try:
        return otp_cache[email]
    except:
        raise HTTPException(status_code=401,detail="OTP Invalid")



if __name__=='__main__':
    print(add_to_otp_cache("sakthi",56565))
    print(get_from_otp_cache("sakthi"))
    print(add_to_otp_cache("sakthi",56565))
