from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.app_setting import AppSetting
from app.models.repository import Repository
from app.services.sync_service import SyncService


@dataclass
class SchedulerPlan:
    sync_interval_minutes: int
    analysis_interval_minutes: int


class SchedulerRunner:
    def __init__(self, session: Session, sync_service: SyncService | None = None) -> None:
        self.session = session
        self.sync_service = sync_service or SyncService(session)

    def build_plan(self) -> SchedulerPlan:
        sync_interval = self._get_setting("sync_interval_minutes", 60)
        analysis_interval = self._get_setting("analysis_interval_minutes", 240)

        return SchedulerPlan(
            sync_interval_minutes=sync_interval,
            analysis_interval_minutes=analysis_interval,
        )

    def run_sync_cycle(self) -> None:
        for repository in self.session.scalars(select(Repository).where(Repository.enabled.is_(True))).all():
            self.sync_service.sync_repository(repository.full_name)

    def run_analysis_cycle(self) -> None:
        for repository in self.session.scalars(select(Repository).where(Repository.enabled.is_(True))).all():
            self.sync_service.analyze_repository(repository.id)

    def _get_setting(self, key: str, default: int) -> int:
        setting = self.session.get(AppSetting, key)
        return int(setting.value) if setting is not None else default
