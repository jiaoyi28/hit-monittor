from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

import app.models
from app.core.database import Base, seed_default_settings
from app.main import app


@pytest.fixture
def engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        seed_default_settings(session)
    yield engine
    engine.dispose()


@pytest.fixture
def client(engine) -> Generator[TestClient]:
    from app.core.database import get_session

    def override_get_session() -> Generator[Session]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def session(engine) -> Generator[Session]:
    with Session(engine) as current_session:
        yield current_session
