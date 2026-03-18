from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session

import app.models
from app.core.database import Base, seed_default_settings, session_scope


@pytest.fixture
def session() -> Generator[Session]:
    with session_scope("sqlite:///:memory:") as current_session:
        Base.metadata.create_all(current_session.bind)
        seed_default_settings(current_session)
        yield current_session
