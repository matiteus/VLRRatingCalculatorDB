"""ORM model for the ``val_matches`` table representing a scraped VLR match."""

import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Integer,
    String,
    false,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from VLRRatingCalculatorDB.model.base import Base


class MatchModel(Base):
    """Model of the Match table."""

    __tablename__ = "val_matches"
    __table_args__ = (
        CheckConstraint(
            "glicko_error >= 0",
            name="ck_val_matches_glicko_error_nonnegative",
        ),
    )
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    vlr_match_id: Mapped[int] = mapped_column(Integer, unique=True)
    link: Mapped[str] = mapped_column(String, index=True)
    # Indexed for date-range reads (Forecast) and date-ordered processing (Glicko).
    match_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, index=True)
    extracted_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    has_issue: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # Match header. NULL for matches scraped before these were extracted.
    event_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    event_name: Mapped[str | None] = mapped_column(String, nullable=True)
    event_stage: Mapped[str | None] = mapped_column(String, nullable=True)
    series_format: Mapped[str | None] = mapped_column(String, nullable=True)  # "Bo1" / "Bo3" / "Bo5"
    patch: Mapped[str | None] = mapped_column(String, nullable=True)  # "13.06"
    team_1_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    team_1_name: Mapped[str | None] = mapped_column(String, nullable=True)
    team_2_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    team_2_name: Mapped[str | None] = mapped_column(String, nullable=True)
    glicko_processed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=false(),
    )
    glicko_error: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
    )