from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "databaseAVB.db"


class Settings(BaseSettings):
    app_env: str = "dev"
    app_name: str = "Dealer MVP"
    app_base_url: str = "http://localhost:8000"
    database_url: str = Field(default=f"sqlite:///{DEFAULT_DB_PATH.as_posix()}")
    openrouter_api_key: str
    openrouter_model: str = "meta-llama/llama-3.1-8b-instruct:free"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
