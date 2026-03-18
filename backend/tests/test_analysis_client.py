from types import SimpleNamespace

from app.core.config import Settings
from app.services.analysis_client import AnalysisClient, create_analysis_client


class StubCompletions:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content='{"summary":"Structured summary","hotspots":["issue"],"watch":true}'
                    )
                )
            ]
        )


class StubSdkClient:
    def __init__(self) -> None:
        self.completions = StubCompletions()
        self.chat = SimpleNamespace(completions=self.completions)


def test_create_analysis_client_returns_none_without_api_key() -> None:
    settings = Settings()

    assert create_analysis_client(settings) is None


def test_analysis_client_uses_openai_sdk_and_parses_json() -> None:
    sdk_client = StubSdkClient()
    client = AnalysisClient(
        api_key="sk-test",
        base_url="https://api.openai.com/v1",
        model="gpt-4.1-mini",
        sdk_client=sdk_client,
    )

    payload = client.analyze("Summarize repository activity")

    assert payload["summary"] == "Structured summary"
    assert sdk_client.completions.calls == [
        {
            "model": "gpt-4.1-mini",
            "messages": [{"role": "user", "content": "Summarize repository activity"}],
            "response_format": {"type": "json_object"},
        }
    ]
