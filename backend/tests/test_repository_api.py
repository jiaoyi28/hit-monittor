from app.models.app_setting import AppSetting
from app.models.issue import Issue
from app.models.pull_request import PullRequest
from app.models.release import Release
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


def test_get_repository_detail_returns_issue_pr_and_release_sections(session, client) -> None:
    repository = Repository(
        owner="openai",
        name="openai-python",
        full_name="openai/openai-python",
        description="Python library for the OpenAI API",
        html_url="https://github.com/openai/openai-python",
    )
    session.add(repository)
    session.flush()

    session.add(
        Issue(
            github_id=11,
            repository_id=repository.id,
            title="Issue title",
            state="open",
            comments_count=4,
            html_url="https://github.com/openai/openai-python/issues/11",
            summary_text="Issue summary",
        )
    )
    session.add(
        PullRequest(
            github_id=22,
            repository_id=repository.id,
            title="PR title",
            state="open",
            comments_count=6,
            review_count=2,
            html_url="https://github.com/openai/openai-python/pull/22",
            summary_text="PR summary",
        )
    )
    session.add(
        Release(
            github_id=33,
            repository_id=repository.id,
            tag_name="v1.0.0",
            title="1.0.0",
            html_url="https://github.com/openai/openai-python/releases/tag/v1.0.0",
            summary_text="Release summary",
        )
    )
    session.commit()

    response = client.get(f"/api/repositories/{repository.id}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["repository"]["full_name"] == "openai/openai-python"
    assert payload["issues"][0]["title"] == "Issue title"
    assert payload["pull_requests"][0]["title"] == "PR title"
    assert payload["releases"][0]["title"] == "1.0.0"
