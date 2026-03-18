from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.issue import Issue
from app.models.pull_request import PullRequest
from app.models.release import Release
from app.models.repository import Repository
from app.schemas.repository import (
    RepositoryDetailItem,
    RepositoryDetailResponse,
    RepositoryDetailSummary,
    RepositoryListItem,
)


class RepositoryService:
    def list_repositories(self, session: Session) -> list[RepositoryListItem]:
        repositories = session.scalars(select(Repository).order_by(Repository.id)).all()
        return [
            RepositoryListItem(
                id=item.id,
                full_name=item.full_name,
                description=item.description,
                html_url=item.html_url,
                enabled=item.enabled,
            )
            for item in repositories
        ]

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
