from app.core.config import Settings
from app.core.database import initialize_database
from app.models.app_setting import AppSetting


def test_default_database_path_uses_d_sqlite() -> None:
    settings = Settings()

    assert str(settings.database_path) == r"D:\sqlite\hit-monittor.db"


def test_settings_reads_openai_environment_variables(monkeypatch) -> None:
    monkeypatch.setenv("HIT_MONITTOR_OPENAI_BASE_URL", "https://api.openai.com/v1")
    monkeypatch.setenv("HIT_MONITTOR_OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("HIT_MONITTOR_OPENAI_MODEL", "gpt-4.1-mini")

    settings = Settings()

    assert settings.openai_base_url == "https://api.openai.com/v1"
    assert settings.openai_api_key == "sk-test"
    assert settings.openai_model == "gpt-4.1-mini"


def test_initialize_database_creates_sqlite_file_and_seeds_defaults(tmp_path) -> None:
    settings = Settings(database_dir=tmp_path, database_name="test.db")

    engine = initialize_database(settings)

    with engine.begin() as connection:
        result = connection.execute(AppSetting.__table__.select())
        rows = result.fetchall()

    assert settings.database_path.exists()
    assert any(row.key == "sync_interval_minutes" for row in rows)
