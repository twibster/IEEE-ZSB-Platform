from fastapi import Depends, HTTPException, status
from backend import db
from backend.models import User
from backend.functions import decodeToken


async def getCurrentUser(token: str) -> User:
    payload = decodeToken(token)
    if payload:
        user = db.query(User).filter_by(id=payload.get("id")).first()
        if user:
            return user
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid payload")


class roleChecker:
    def __init__(self, requiredRole):
        self.requiredRole: str = requiredRole

    def __call__(self, user: User = Depends(getCurrentUser)) -> User:
        if self.requiredRole == user.position:
            return user
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "you do not have permission for this request")
