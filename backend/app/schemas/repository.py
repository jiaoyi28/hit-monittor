from pydantic import BaseModel


class RepositoryCreateRequest(BaseModel):
    url: str


class RepositoryListItem(BaseModel):
    id: int
    full_name: str
    description: str | None = None
    html_url: str
    enabled: bool


class RepositoryDetailItem(BaseModel):
    title: str
    url: str
    summary: str | None = None


class RepositoryDetailSummary(BaseModel):
    id: int
    full_name: str
    description: str | None = None
    html_url: str


class RepositoryDetailResponse(BaseModel):
    repository: RepositoryDetailSummary
    issues: list[RepositoryDetailItem]
    pull_requests: list[RepositoryDetailItem]
    releases: list[RepositoryDetailItem]
