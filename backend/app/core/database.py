from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import Settings, get_settings


class Base(DeclarativeBase):
    pass


DEFAULT_SETTINGS = {
    "sync_interval_minutes": "60",
    "analysis_interval_minutes": "240",
    "analysis_candidate_limit": "10",
}


def create_sqlite_url(settings: Settings) -> str:
    return f"sqlite:///{settings.database_path.as_posix()}"


def create_engine_from_settings(settings: Settings | None = None):
    resolved_settings = settings or get_settings()
    return create_engine(create_sqlite_url(resolved_settings), future=True)


engine = create_engine_from_settings()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@contextmanager
def session_scope(database_url: str | None = None) -> Generator[Session]:
    if database_url is None:
        engine = create_engine_from_settings()
    else:
        engine = create_engine(database_url, future=True)

    with Session(engine) as session:
        yield session


def get_session() -> Generator[Session]:
    with SessionLocal() as session:
        yield session


def seed_default_settings(session: Session) -> None:
    from app.models.app_setting import AppSetting

    for key, value in DEFAULT_SETTINGS.items():
        existing = session.get(AppSetting, key)
        if existing is None:
            session.add(AppSetting(key=key, value=value))

    session.commit()
