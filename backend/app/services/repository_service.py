from urllib.parse import urlparse

from fastapi import HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.issue import Issue
from app.models.pull_request import PullRequest
from app.models.release import Release
from app.models.repository import Repository
from app.services.github_client import GitHubClient
from app.services.ingestion import GitHubIngestionService
from app.schemas.repository import (
    RepositoryDetailItem,
    RepositoryDetailResponse,
    RepositoryDetailSummary,
    RepositoryListItem,
)


class RepositoryService:
    def list_repositories(self, session: Session) -> list[RepositoryListItem]:
        repositories = session.scalars(select(Repository).order_by(Repository.id)).all()
        return [self._to_list_item(item) for item in repositories]

    def add_repository_from_url(
        self,
        session: Session,
        url: str,
        github_client: GitHubClient | None = None,
    ) -> RepositoryListItem:
        full_name = self._extract_full_name(url)
        client = github_client or GitHubClient()
        GitHubIngestionService(session=session, client=client).sync_repository(full_name)

        repository = session.scalar(select(Repository).where(Repository.full_name == full_name))
        if repository is None:
            raise HTTPException(status_code=502, detail="Repository sync completed without storing repository data")

        return self._to_list_item(repository)

    def get_repository_detail(self, session: Session, repository_id: int) -> RepositoryDetailResponse:
        repository = session.get(Repository, repository_id)
        issues = session.scalars(
            select(Issue).where(Issue.repository_id == repository_id).order_by(desc(Issue.comments_count), Issue.id)
        ).all()
        pull_requests = session.scalars(
            select(PullRequest).where(PullRequest.repository_id == repository_id).order_by(desc(PullRequest.comments_count), PullRequest.id)
        ).all()
        releases = session.scalars(
            select(Release).where(Release.repository_id == repository_id).order_by(desc(Release.id))
        ).all()

        return RepositoryDetailResponse(
            repository=RepositoryDetailSummary(
                id=repository.id,
                full_name=repository.full_name,
                description=repository.description,
                html_url=repository.html_url,
            ),
            issues=[RepositoryDetailItem(title=item.title, url=item.html_url, summary=item.summary_text) for item in issues],
            pull_requests=[RepositoryDetailItem(title=item.title, url=item.html_url, summary=item.summary_text) for item in pull_requests],
            releases=[
                RepositoryDetailItem(
                    title=item.title or item.tag_name,
                    url=item.html_url,
                    summary=item.summary_text,
                )
                for item in releases
            ],
        )

    @staticmethod
    def _extract_full_name(url: str) -> str:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or parsed.netloc not in {"github.com", "www.github.com"}:
            raise HTTPException(status_code=400, detail="Only GitHub repository URLs are supported")

        segments = [segment for segment in parsed.path.split("/") if segment]
        if len(segments) < 2:
            raise HTTPException(status_code=400, detail="Repository URL must include owner and repository name")

        return f"{segments[0]}/{segments[1]}"

    @staticmethod
    def _to_list_item(item: Repository) -> RepositoryListItem:
        return RepositoryListItem(
            id=item.id,
            full_name=item.full_name,
            description=item.description,
            html_url=item.html_url,
            enabled=item.enabled,
        )
