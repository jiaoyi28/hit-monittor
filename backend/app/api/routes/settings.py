from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.settings import SettingsResponse, SettingsUpdate
from app.services.settings_service import SettingsService

router = APIRouter(prefix="/api/settings", tags=["settings"])
SessionDep = Annotated[Session, Depends(get_session)]
settings_service = SettingsService()


@router.get("", response_model=SettingsResponse)
def get_settings(session: SessionDep) -> SettingsResponse:
    return settings_service.get(session)


@router.patch("", response_model=SettingsResponse)
def update_settings(payload: SettingsUpdate, session: SessionDep) -> SettingsResponse:
    return settings_service.update(session, payload)
