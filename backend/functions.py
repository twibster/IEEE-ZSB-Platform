from typing import Optional
from datetime import timedelta, datetime
from jose import JWTError, jwt

SECRET_KEY = "1jgRFeMmP2vlXWbzUxUlnbEey85meU4n"
ALOGRITHM = "HS256"
EXPIRY = 30

create_payload = lambda user: {
    "id":user.id,
    "username": user.username
}

def generateToken(payload: dict, expiry_duration: int = EXPIRY) -> str:
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expiry_duration)
    encoded_jwt = jwt.encode(payload, SECRET_KEY, ALOGRITHM)
    return encoded_jwt

def decodeToken(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY)
    except JWTError:
        return None
    return payload
