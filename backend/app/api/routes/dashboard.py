from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])
SessionDep = Annotated[Session, Depends(get_session)]
dashboard_service = DashboardService()


@router.get("", response_model=DashboardResponse)
def get_dashboard(session: SessionDep) -> DashboardResponse:
    return dashboard_service.get_dashboard(session)
