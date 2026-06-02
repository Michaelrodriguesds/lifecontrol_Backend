from pydantic_settings import BaseSettings


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

    # ⚠️ PROBLEMA CORRIGIDO:
    # O padrão era DEV_MODE: bool = True
    # Isso significa que MESMO com DEV_MODE=false no .env,
    # o Python usava True porque o Pydantic não estava lendo o arquivo.
    # A causa era a falta do env_file na classe Config.
    # Com env_file=".env", o Pydantic lê o arquivo e respeita DEV_MODE=false.
    DEV_MODE: bool = False  # padrão seguro; o .env sobrescreve se necessário

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
