from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.issue import Issue
from app.models.pull_request import PullRequest
from app.models.release import Release
from app.schemas.dashboard import DashboardResponse, HotItem


class DashboardService:
    def get_dashboard(self, session: Session) -> DashboardResponse:
        hot_issues = session.scalars(select(Issue).order_by(desc(Issue.comments_count)).limit(5)).all()
        hot_pull_requests = session.scalars(select(PullRequest).order_by(desc(PullRequest.comments_count)).limit(5)).all()
        latest_releases = session.scalars(select(Release).order_by(desc(Release.id)).limit(5)).all()

        return DashboardResponse(
            hot_issues=[HotItem(title=item.title, url=item.html_url, summary=item.summary_text) for item in hot_issues],
            hot_pull_requests=[HotItem(title=item.title, url=item.html_url, summary=item.summary_text) for item in hot_pull_requests],
            latest_releases=[HotItem(title=item.title or item.tag_name, url=item.html_url, summary=item.summary_text) for item in latest_releases],
        )
