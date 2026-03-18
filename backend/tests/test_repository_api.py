from app.models.app_setting import AppSetting
from app.models.repository import Repository


def test_default_settings_seed_intervals(session) -> None:
    settings = session.query(AppSetting).all()

    assert any(item.key == "sync_interval_minutes" for item in settings)
    assert any(item.key == "analysis_interval_minutes" for item in settings)


def test_get_dashboard_returns_hot_sections(client) -> None:
    response = client.get("/api/dashboard")

    assert response.status_code == 200
    payload = response.json()
    assert "hot_issues" in payload
    assert "hot_pull_requests" in payload
    assert "latest_releases" in payload


def test_list_repositories_returns_saved_repository(session, client) -> None:
    session.add(
        Repository(
            owner="openai",
            name="openai-python",
            full_name="openai/openai-python",
            description="Python library for the OpenAI API",
            html_url="https://github.com/openai/openai-python",
        )
    )
    session.commit()

    response = client.get("/api/repositories")

    assert response.status_code == 200
    assert response.json()[0]["full_name"] == "openai/openai-python"
