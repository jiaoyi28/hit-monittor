from typing import Any

from sqlalchemy.orm import Session

from app.services.analysis_pipeline import AnalysisPipeline
from app.services.analysis_client import create_analysis_client
from app.services.github_client import GitHubClient
from app.services.ingestion import GitHubIngestionService


class SyncService:
    def __init__(
        self,
        session: Session,
        github_client: GitHubClient | None = None,
        analysis_client: Any | None = None,
    ) -> None:
        self.session = session
        self.github_client = github_client or GitHubClient()
        self.analysis_client = analysis_client or create_analysis_client()

    def sync_repository(self, full_name: str) -> None:
        GitHubIngestionService(session=self.session, client=self.github_client).sync_repository(full_name)

    def analyze_repository(self, repository_id: int) -> dict[str, Any]:
        if self.analysis_client is None:
            raise RuntimeError("Analysis client is not configured")

        return AnalysisPipeline(session=self.session, client=self.analysis_client).analyze_repository(repository_id)
