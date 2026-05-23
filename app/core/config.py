from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # MongoDB
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "lifecontrol"

    # JWT
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # App
    APP_NAME: str = "LifeControl"
    DEBUG: bool = True
    FRONTEND_URL: str = "http://localhost:4200"

    # Dev Mode — desativa autenticação obrigatória
    DEV_MODE: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
