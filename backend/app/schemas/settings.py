from pydantic import BaseModel


class SettingsUpdate(BaseModel):
    sync_interval_minutes: int | None = None
    analysis_interval_minutes: int | None = None


class SettingsResponse(BaseModel):
    sync_interval_minutes: int
    analysis_interval_minutes: int
