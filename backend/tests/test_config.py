from app.core.config import Settings


def test_default_database_path_uses_d_sqlite() -> None:
    settings = Settings()

    assert str(settings.database_path) == r"D:\sqlite\hit-monittor.db"
