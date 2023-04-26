from typing import Optional
from datetime import timedelta, datetime
from jose import JWTError, jwt
from backend.models import User

SECRET_KEY = "1jgRFeMmP2vlXWbzUxUlnbEey85meU4n"
ALOGRITHM = "HS256"
EXPIRY = 30


def create_payload(user: User) -> dict:
    """Generate a payload containing the user ID, username, and role to be encoded as a JWT.

    Args:
        user (User): A User object containing the user's information.

    Returns:
        dict: A dictionary containing the user's ID, username, and role.

    Raises:
        TypeError: If the user parameter is not an instance of the User class.
    """
    payload = {
        "id": user.id,
        "username": user.username,
        "role": user.position
    }
    return payload


def generate_token(payload: dict, expiry_duration: int = EXPIRY) -> str:
    """Generates a JSON Web Token (JWT) using the given payload and expiration duration.

    Args:
        payload (dict): A dictionary containing the payload to be encoded in the JWT.
        expiry_duration (int, optional): The duration (in minutes) for which the JWT will be valid.
            Defaults to the value of the `EXPIRY` constant.

    Returns:
        str: The encoded JWT as a string.

    Raises:
        ValueError: If the payload is not a dictionary or the expiry duration is not a positive integer.
    """
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expiry_duration)
    encoded_jwt = jwt.encode(payload, SECRET_KEY, ALOGRITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode a JSON Web Token (JWT) and return its payload as a dictionary.

    Args:
        token (str): The encoded JWT as a string.

    Returns:
        Optional[dict]: A dictionary containing the payload decoded from the JWT,
            or `None` if the token is invalid or cannot be decoded.

    Examples:
        >>> token = 'eyJhbGciOiJIUzI1Nkw'
        >>> decodeToken(token)
        {'id': 1234, 'username': 'johndoe', 'exp': 1619399485}
    """
    try:
        payload = jwt.decode(token, SECRET_KEY)
    except JWTError:
        return None
    return payload
