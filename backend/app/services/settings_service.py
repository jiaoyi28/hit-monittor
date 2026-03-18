from sqlalchemy.orm import Session

from app.models.app_setting import AppSetting
from app.schemas.settings import SettingsResponse, SettingsUpdate


class SettingsService:
    def get(self, session: Session) -> SettingsResponse:
        return SettingsResponse(
            sync_interval_minutes=int(session.get(AppSetting, "sync_interval_minutes").value),
            analysis_interval_minutes=int(session.get(AppSetting, "analysis_interval_minutes").value),
        )

    def update(self, session: Session, payload: SettingsUpdate) -> SettingsResponse:
        if payload.sync_interval_minutes is not None:
            session.get(AppSetting, "sync_interval_minutes").value = str(payload.sync_interval_minutes)
        if payload.analysis_interval_minutes is not None:
            session.get(AppSetting, "analysis_interval_minutes").value = str(payload.analysis_interval_minutes)

        session.commit()
        return self.get(session)
