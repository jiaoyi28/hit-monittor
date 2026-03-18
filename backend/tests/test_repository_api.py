from app.models.app_setting import AppSetting


def test_default_settings_seed_intervals(session) -> None:
    settings = session.query(AppSetting).all()

    assert any(item.key == "sync_interval_minutes" for item in settings)
    assert any(item.key == "analysis_interval_minutes" for item in settings)
