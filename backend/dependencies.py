from fastapi import Depends, HTTPException, status
from backend import db
from backend.functions import decode_token
from backend.database.models import User


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
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user in the palyload is not found")
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid or expired token")


class PermissionsChecker:
    """A class used to check a user's permission and grant access to a specific endpoint.

    Attributes:
        requiredPermission (str): The required permission for accessing an endpoint.

    Methods:
        __init__(self, requiredPermission: str) -> None: Initializes the required Permission for the endpoint.
        __call__(self, user: User = Depends(getCurrentUser)) -> User: Verifies that the user
            has a Permission that matches the required role before granting access to an endpoint.
    """
    def __init__(self, required_permission):
        self.required_permission: str = required_permission

    def __call__(self, user: User = Depends(get_current_user)) -> User:
        if getattr(user.permissions, self.required_permission):
            return user
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "you do not have permission for this request")
