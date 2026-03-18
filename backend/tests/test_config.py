from app.core.config import Settings
from app.core.database import initialize_database
from app.models.app_setting import AppSetting


def test_default_database_path_uses_d_sqlite() -> None:
    settings = Settings()

    assert str(settings.database_path) == r"D:\sqlite\hit-monittor.db"


def test_initialize_database_creates_sqlite_file_and_seeds_defaults(tmp_path) -> None:
    settings = Settings(database_dir=tmp_path, database_name="test.db")

    engine = initialize_database(settings)

    with engine.begin() as connection:
        result = connection.execute(AppSetting.__table__.select())
        rows = result.fetchall()

    assert settings.database_path.exists()
    assert any(row.key == "sync_interval_minutes" for row in rows)
