from typing import Any

import httpx


class GitHubClient:
    def __init__(self, base_url: str = "https://api.github.com") -> None:
        self._client = httpx.Client(base_url=base_url, headers={"Accept": "application/vnd.github+json"})

    def fetch_repository_bundle(self, full_name: str) -> dict[str, Any]:
        return {
            "repository": self._get(f"/repos/{full_name}"),
            "issues": self._get(f"/repos/{full_name}/issues"),
            "pulls": self._get(f"/repos/{full_name}/pulls"),
            "releases": self._get(f"/repos/{full_name}/releases"),
        }

    def _get(self, path: str) -> Any:
        response = self._client.get(path)
        response.raise_for_status()
        return response.json()
