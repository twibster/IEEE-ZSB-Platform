import os
from typing import Union


class Config:
    DATABASE_URI: str = os.environ.get("DATABASE_URI", "sqlite:///platform.db")
    SECRET_KEY: Union[str, None] = os.environ.get("SECRET_KEY")
    JWT_ALGO: str = os.environ.get("JWT_ALGO", "HS256")
    JWT_EXPIREY: int = int(os.environ.get("JWT_EXPIREY", 30))

    @classmethod
    def validate_variables(cls) -> None:
        if not cls.SECRET_KEY:
            raise ValueError("A secret key must be present in the enviornment variables")
        if cls.JWT_ALGO not in ['HS256', 'HS384', 'HS512', 'RS256', 'RS384', 'RS512', 'ES256', 'ES384', 'ES512']:
            raise ValueError("Not a valid JWT algorithm")


Config.validate_variables()
