from fastapi import Depends, HTTPException, status
from backend import db
from backend.models import User
from backend.functions import decodeToken

async def getCurrentUser(token: str) -> User:
    payload = decodeToken(token)
    if payload:
        user = db.query(User).filter_by(id = payload.get("id")).first()
        if user:
            return user
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")
    raise HTTPException(status.HTTP_401_UNAUTHORIZED)

async def leaderRequired(user: User = Depends(getCurrentUser)) -> User:
    if user.position == "leader":
        return user
    raise HTTPException(status.HTTP_401_UNAUTHORIZED)

async def memberRequired(user: User = Depends(getCurrentUser)) -> User:
    if user.position == "member":
        return user
    raise HTTPException(status.HTTP_401_UNAUTHORIZED)