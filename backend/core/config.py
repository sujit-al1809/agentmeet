from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/  -> this file is backend/core/config.py, so parent.parent = backend/
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    OPENAI_API_KEY: str = ""
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    # Point env_file at backend/.env explicitly so it is found no matter
    # which directory the app is launched from.
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()
