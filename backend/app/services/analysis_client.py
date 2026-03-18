import json
from typing import Any

from openai import OpenAI

from app.core.config import Settings, get_settings


class AnalysisClient:
    def __init__(self, api_key: str, model: str, base_url: str | None = None, sdk_client: Any | None = None) -> None:
        self.base_url = base_url.rstrip("/") if base_url else None
        self.api_key = api_key
        self.model = model
        self.sdk_client = sdk_client or OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def analyze(self, prompt: str) -> dict[str, Any]:
        response = self.sdk_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        return content if isinstance(content, dict) else json.loads(content)


def create_analysis_client(settings: Settings | None = None) -> AnalysisClient | None:
    resolved_settings = settings or get_settings()
    if not resolved_settings.openai_api_key:
        return None

    return AnalysisClient(
        api_key=resolved_settings.openai_api_key,
        base_url=resolved_settings.openai_base_url,
        model=resolved_settings.openai_model,
    )
