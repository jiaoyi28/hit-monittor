from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.repository import RepositoryCreateRequest, RepositoryDetailResponse, RepositoryListItem
from app.services.repository_service import RepositoryService

router = APIRouter(prefix="/api/repositories", tags=["repositories"])
SessionDep = Annotated[Session, Depends(get_session)]
repository_service = RepositoryService()


@router.get("", response_model=list[RepositoryListItem])
def list_repositories(session: SessionDep) -> list[RepositoryListItem]:
    return repository_service.list_repositories(session)


@router.post("", response_model=RepositoryListItem, status_code=status.HTTP_201_CREATED)
def add_repository(payload: RepositoryCreateRequest, session: SessionDep) -> RepositoryListItem:
    return repository_service.add_repository_from_url(session, payload.url)


@router.get("/{repository_id}", response_model=RepositoryDetailResponse)
def get_repository_detail(repository_id: int, session: SessionDep) -> RepositoryDetailResponse:
    return repository_service.get_repository_detail(session, repository_id)
