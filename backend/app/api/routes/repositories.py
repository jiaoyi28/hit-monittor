from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.models.repository import Repository
from app.schemas.repository import RepositoryListItem

router = APIRouter(prefix="/api/repositories", tags=["repositories"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("", response_model=list[RepositoryListItem])
def list_repositories(session: SessionDep) -> list[RepositoryListItem]:
    repositories = session.scalars(select(Repository).order_by(Repository.id)).all()
    return [
        RepositoryListItem(
            id=item.id,
            full_name=item.full_name,
            description=item.description,
            html_url=item.html_url,
            enabled=item.enabled,
        )
        for item in repositories
    ]
