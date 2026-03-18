from pydantic import BaseModel


class HotItem(BaseModel):
    title: str
    url: str
    summary: str | None = None


class DashboardResponse(BaseModel):
    hot_issues: list[HotItem]
    hot_pull_requests: list[HotItem]
    latest_releases: list[HotItem]
