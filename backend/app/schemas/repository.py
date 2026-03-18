from pydantic import BaseModel


class RepositoryListItem(BaseModel):
    id: int
    full_name: str
    description: str | None = None
    html_url: str
    enabled: bool
