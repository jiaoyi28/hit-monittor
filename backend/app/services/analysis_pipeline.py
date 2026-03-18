import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.analysis_result import AnalysisResult
from app.models.issue import Issue
from app.models.pull_request import PullRequest
from app.models.release import Release
from app.models.repository import Repository


class AnalysisPipeline:
    def __init__(self, session: Session, client: Any) -> None:
        self.session = session
        self.client = client

    def analyze_repository(self, repository_id: int) -> dict[str, Any]:
        repository = self.session.get(Repository, repository_id)
        issues = self.session.scalars(select(Issue).where(Issue.repository_id == repository_id)).all()
        pull_requests = self.session.scalars(select(PullRequest).where(PullRequest.repository_id == repository_id)).all()
        releases = self.session.scalars(select(Release).where(Release.repository_id == repository_id)).all()

        prompt = self.build_repository_prompt(repository, issues, pull_requests, releases)
        result = self.client.analyze(prompt)

        record = AnalysisResult(
            object_type="repository",
            object_id=repository_id,
            analysis_type="summary",
            payload_json=json.dumps(result, ensure_ascii=False),
        )
        self.session.add(record)
        self.session.commit()

        return result

    @staticmethod
    def build_repository_prompt(
        repository: Repository,
        issues: list[Issue],
        pull_requests: list[PullRequest],
        releases: list[Release],
    ) -> str:
        return json.dumps(
            {
                "repository": {
                    "full_name": repository.full_name,
                    "description": repository.description,
                },
                "issues": [
                    {
                        "title": issue.title,
                        "comments_count": issue.comments_count,
                        "summary_text": issue.summary_text,
                    }
                    for issue in issues
                ],
                "pull_requests": [
                    {
                        "title": pull_request.title,
                        "comments_count": pull_request.comments_count,
                        "review_count": pull_request.review_count,
                        "summary_text": pull_request.summary_text,
                    }
                    for pull_request in pull_requests
                ],
                "releases": [
                    {
                        "tag_name": release.tag_name,
                        "title": release.title,
                        "summary_text": release.summary_text,
                    }
                    for release in releases
                ],
            },
            ensure_ascii=False,
        )
