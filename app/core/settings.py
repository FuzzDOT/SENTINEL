from pydantic import BaseSettings, Field
from typing import Optional


class Settings(BaseSettings):
    ENV: str = Field("development", env="ENV")
    APP_NAME: str = "quant-market-predictor"
    VERSION: str = "0.1.0"

    # Database (use str to allow sqlite in-memory URLs during tests)
    DATABASE_URL: str

    # Redis
    REDIS_URL: Optional[str] = None

    # S3 / MinIO
    S3_ENDPOINT: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_BUCKET: Optional[str] = None

    # Security
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    class Config:
        env_file = ".env"
        case_sensitive = True


# Lazy settings: constructing Settings() may require env vars; use a lazy loader so
# modules (like alembic/env.py) can import without causing validation errors at
# import time. Accessing attributes will create the real Settings instance on
# first use.
class _LazySettings:
    _instance: Optional[Settings] = None

    def _load(self) -> Settings:
        if self._instance is None:
            self._instance = Settings()
        return self._instance

    def __getattr__(self, item):
        return getattr(self._load(), item)


settings = _LazySettings()
