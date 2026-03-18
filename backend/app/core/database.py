from sqlalchemy import create_engine

from app.core.config import Settings, get_settings


def create_sqlite_url(settings: Settings) -> str:
    return f"sqlite:///{settings.database_path.as_posix()}"


def create_engine_from_settings(settings: Settings | None = None):
    resolved_settings = settings or get_settings()
    return create_engine(create_sqlite_url(resolved_settings), future=True)
