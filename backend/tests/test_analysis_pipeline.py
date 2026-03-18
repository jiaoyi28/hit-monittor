import json

from app.models.analysis_result import AnalysisResult
from app.models.issue import Issue
from app.models.pull_request import PullRequest
from app.models.release import Release
from app.models.repository import Repository
from app.services.analysis_pipeline import AnalysisPipeline


class StubAnalysisClient:
    def analyze(self, prompt: str) -> dict:
        payload = json.loads(prompt)

        assert payload["repository"]["full_name"] == "openai/openai-python"
        assert len(payload["issues"]) == 1
        assert len(payload["pull_requests"]) == 1
        assert len(payload["releases"]) == 1

        return {
            "summary": "SDK issue and PR discussion are both active.",
            "hotspots": ["issue", "pull_request"],
            "watch": True,
        }


def test_analysis_pipeline_saves_structured_summary(session) -> None:
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
            comments_count=10,
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

    pipeline = AnalysisPipeline(session=session, client=StubAnalysisClient())

    result = pipeline.analyze_repository(repository.id)
    saved = session.query(AnalysisResult).one()

    assert result["summary"] == "SDK issue and PR discussion are both active."
    assert saved.object_type == "repository"
    assert saved.analysis_type == "summary"
