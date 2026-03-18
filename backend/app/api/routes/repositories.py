from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.repository import RepositoryDetailResponse, RepositoryListItem
from app.services.repository_service import RepositoryService

router = APIRouter(prefix="/api/repositories", tags=["repositories"])
SessionDep = Annotated[Session, Depends(get_session)]
repository_service = RepositoryService()


@router.get("", response_model=list[RepositoryListItem])
def list_repositories(session: SessionDep) -> list[RepositoryListItem]:
    return repository_service.list_repositories(session)


@router.get("/{repository_id}", response_model=RepositoryDetailResponse)
def get_repository_detail(repository_id: int, session: SessionDep) -> RepositoryDetailResponse:
    return repository_service.get_repository_detail(session, repository_id)
