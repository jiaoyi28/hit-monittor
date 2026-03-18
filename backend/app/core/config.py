from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HIT_MONITTOR_", extra="ignore")

    database_dir: Path = Path(r"D:\sqlite")
    database_name: str = "hit-monittor.db"
    openai_base_url: str | None = None
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"

    @property
    def database_path(self) -> Path:
        return self.database_dir / self.database_name


@lru_cache
def get_settings() -> Settings:
    return Settings()
