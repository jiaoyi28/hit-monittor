from app.models.issue import Issue
from app.models.pull_request import PullRequest
from app.models.release import Release
from app.models.repository import Repository
from app.services.ingestion import GitHubIngestionService


class StubGitHubClient:
    def fetch_repository_bundle(self, full_name: str) -> dict:
        assert full_name == "openai/openai-python"

        return {
            "repository": {
                "owner": {"login": "openai"},
                "name": "openai-python",
                "full_name": full_name,
                "description": "Python library for the OpenAI API",
                "html_url": "https://github.com/openai/openai-python",
            },
            "issues": [
                {
                    "id": 101,
                    "title": "Bug report",
                    "state": "open",
                    "labels": [{"name": "bug"}],
                    "comments": 12,
                    "user": {"login": "alice"},
                    "html_url": "https://github.com/openai/openai-python/issues/101",
                    "body": "Broken behavior",
                    "created_at": "2026-03-18T00:00:00Z",
                    "updated_at": "2026-03-18T01:00:00Z",
                }
            ],
            "pulls": [
                {
                    "id": 202,
                    "title": "Add feature",
                    "state": "open",
                    "comments": 5,
                    "requested_reviewers": [{"login": "bob"}],
                    "user": {"login": "carol"},
                    "merged_at": None,
                    "html_url": "https://github.com/openai/openai-python/pull/202",
                    "body": "Implements feature",
                    "created_at": "2026-03-17T00:00:00Z",
                    "updated_at": "2026-03-18T02:00:00Z",
                }
            ],
            "releases": [
                {
                    "id": 303,
                    "tag_name": "v1.0.0",
                    "name": "1.0.0",
                    "html_url": "https://github.com/openai/openai-python/releases/tag/v1.0.0",
                    "body": "Initial stable release",
                    "published_at": "2026-03-16T00:00:00Z",
                }
            ],
        }


def test_ingestion_upserts_repository_issue_pr_release(session) -> None:
    service = GitHubIngestionService(session=session, client=StubGitHubClient())

    result = service.sync_repository("openai/openai-python")

    repository = session.query(Repository).one()
    issue = session.query(Issue).one()
    pull_request = session.query(PullRequest).one()
    release = session.query(Release).one()

    assert result.repository_full_name == "openai/openai-python"
    assert repository.full_name == "openai/openai-python"
    assert issue.github_id == 101
    assert pull_request.github_id == 202
    assert release.github_id == 303
