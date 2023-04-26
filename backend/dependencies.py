from fastapi import Depends, HTTPException, status
from backend import db
from backend.models import User
from backend.functions import decode_token


async def get_current_user(token: str) -> User:
    """Retrieves the current user object based on the provided token.

    Args:
        token (str): A string containing a JSON Web Token (JWT) for the user.

    Returns:
        User: A User object representing the current user.

    Raises:
        HTTPException: If the token is invalid or expired, or if the user cannot be found.
    """
    payload = decode_token(token)
    if payload:
        user = db.query(User).filter_by(id=payload.get("id")).first()
        if user:
            return user
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid payload")


class RoleChecker:
    """A class used to check a user's role and grant access to a specific endpoint.

    Attributes:
        requiredRole (str): The required role for accessing an endpoint.

    Methods:
        __init__(self, requiredRole: str) -> None: Initializes the required role for the endpoint.
        __call__(self, user: User = Depends(getCurrentUser)) -> User: Verifies that the user's
            role matches the required role before granting access to an endpoint.
    """
    def __init__(self, requiredRole):
        self.requiredRole: str = requiredRole

    def __call__(self, user: User = Depends(get_current_user)) -> User:
        if self.requiredRole == user.position:
            return user
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "you do not have permission for this request")
