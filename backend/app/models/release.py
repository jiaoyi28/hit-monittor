from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Release(Base):
    __tablename__ = "releases"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    github_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id"), nullable=False)
    tag_name: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    html_url: Mapped[str] = mapped_column(String(500), nullable=False)
    notes_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
