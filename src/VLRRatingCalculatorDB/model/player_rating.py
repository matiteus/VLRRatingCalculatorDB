"""Persistent current Glicko-2 state for each scraped player."""

import datetime

from sqlalchemy import JSON, DateTime, Float, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from VLRRatingCalculatorDB.model.base import Base


class PlayerRatingModel(Base):
    """The latest rating state for one player.

    ``name`` is the temporary identity key. A stable VLR player id should
    replace it when the scraper starts extracting profile identifiers.
    """

    __tablename__ = "player_ratings"
    # Glicko looks up each player's current snapshot by (name, version).
    __table_args__ = (Index("ix_player_ratings_name_version", "name", "version"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    team: Mapped[str] = mapped_column(String, nullable=False)
    version: Mapped[str] = mapped_column(
        String, nullable=False, default="current"
    )
    match_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    match_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False
    )
    base_rating: Mapped[float] = mapped_column(
        "rating", Float, nullable=False, default=1500.0
    )
    rating_deviation: Mapped[float] = mapped_column(
        Float, nullable=False, default=350.0
    )
    volatility: Mapped[float] = mapped_column(Float, nullable=False, default=0.06)
    modifiers: Mapped[dict[str, float]] = mapped_column(
        JSON, nullable=False, default=dict
    )
    last_match_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.datetime(1900, 1, 1)
    )
    matches_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)