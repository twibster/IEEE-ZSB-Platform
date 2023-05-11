from typing import Union
from pydantic import BaseSettings, validator


class Config(BaseSettings):
    DATABASE_URI: str = "sqlite:///platform.db"
    SECRET_KEY: Union[str, None]
    JWT_ALGO: str = "HS256"
    JWT_EXPIREY: int = 30

    @validator("SECRET_KEY")
    def validate_secret_key(cls, v: str) -> str:
        if not v:
            raise ValueError("A secret key must be present in the enviornment variables")
        return v
    
    @validator("JWT_ALGO")
    def validate_JWT_ALGO(cls, v: str) -> str:
        if v not in ['HS256', 'HS384', 'HS512', 'RS256', 'RS384', 'RS512', 'ES256', 'ES384', 'ES512']:
            raise ValueError("Not a valid JWT algorithm")
        return v
    

configs = Config()
