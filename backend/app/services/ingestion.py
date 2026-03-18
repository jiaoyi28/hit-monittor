from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.issue import Issue
from app.models.pull_request import PullRequest
from app.models.release import Release
from app.models.repository import Repository
from app.services.github_client import GitHubClient


@dataclass
class SyncSummary:
    repository_full_name: str


class GitHubIngestionService:
    def __init__(self, session: Session, client: GitHubClient) -> None:
        self.session = session
        self.client = client

    def sync_repository(self, full_name: str) -> SyncSummary:
        bundle = self.client.fetch_repository_bundle(full_name)
        repository = self._upsert_repository(bundle["repository"])

        self._upsert_issues(repository.id, bundle["issues"])
        self._upsert_pull_requests(repository.id, bundle["pulls"])
        self._upsert_releases(repository.id, bundle["releases"])
        self.session.commit()

        return SyncSummary(repository_full_name=repository.full_name)

    def _upsert_repository(self, payload: dict[str, Any]) -> Repository:
        repository = self.session.scalar(select(Repository).where(Repository.full_name == payload["full_name"]))

        if repository is None:
            repository = Repository(
                owner=payload["owner"]["login"],
                name=payload["name"],
                full_name=payload["full_name"],
                description=payload.get("description"),
                html_url=payload["html_url"],
            )
            self.session.add(repository)
            self.session.flush()
            return repository

        repository.owner = payload["owner"]["login"]
        repository.name = payload["name"]
        repository.description = payload.get("description")
        repository.html_url = payload["html_url"]
        self.session.flush()
        return repository

    def _upsert_issues(self, repository_id: int, issues: list[dict[str, Any]]) -> None:
        for payload in issues:
            issue = self.session.scalar(select(Issue).where(Issue.github_id == payload["id"]))

            if issue is None:
                issue = Issue(github_id=payload["id"], repository_id=repository_id, title=payload["title"], state=payload["state"], html_url=payload["html_url"])
                self.session.add(issue)

            issue.repository_id = repository_id
            issue.title = payload["title"]
            issue.state = payload["state"]
            issue.labels = ",".join(label["name"] for label in payload.get("labels", []))
            issue.comments_count = payload.get("comments", 0)
            issue.author = (payload.get("user") or {}).get("login")
            issue.html_url = payload["html_url"]
            issue.summary_text = payload.get("body")
            issue.created_at = self._parse_datetime(payload.get("created_at"))
            issue.updated_at = self._parse_datetime(payload.get("updated_at"))

    def _upsert_pull_requests(self, repository_id: int, pull_requests: list[dict[str, Any]]) -> None:
        for payload in pull_requests:
            pull_request = self.session.scalar(select(PullRequest).where(PullRequest.github_id == payload["id"]))

            if pull_request is None:
                pull_request = PullRequest(
                    github_id=payload["id"],
                    repository_id=repository_id,
                    title=payload["title"],
                    state=payload["state"],
                    html_url=payload["html_url"],
                )
                self.session.add(pull_request)

            pull_request.repository_id = repository_id
            pull_request.title = payload["title"]
            pull_request.state = payload["state"]
            pull_request.comments_count = payload.get("comments", 0)
            pull_request.review_count = len(payload.get("requested_reviewers", []))
            pull_request.author = (payload.get("user") or {}).get("login")
            pull_request.merged = payload.get("merged_at") is not None
            pull_request.merged_at = self._parse_datetime(payload.get("merged_at"))
            pull_request.html_url = payload["html_url"]
            pull_request.summary_text = payload.get("body")
            pull_request.created_at = self._parse_datetime(payload.get("created_at"))
            pull_request.updated_at = self._parse_datetime(payload.get("updated_at"))

    def _upsert_releases(self, repository_id: int, releases: list[dict[str, Any]]) -> None:
        for payload in releases:
            release = self.session.scalar(select(Release).where(Release.github_id == payload["id"]))

            if release is None:
                release = Release(
                    github_id=payload["id"],
                    repository_id=repository_id,
                    tag_name=payload["tag_name"],
                    html_url=payload["html_url"],
                )
                self.session.add(release)

            release.repository_id = repository_id
            release.tag_name = payload["tag_name"]
            release.title = payload.get("name")
            release.html_url = payload["html_url"]
            release.notes_text = payload.get("body")
            release.summary_text = payload.get("body")
            release.published_at = self._parse_datetime(payload.get("published_at"))

    @staticmethod
    def _parse_datetime(value: str | None) -> datetime | None:
        if value is None:
            return None

        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)
