"""ORM model for the ``val_maps`` table representing a single map within a match."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from VLRRatingCalculatorDB.model.base import Base


class MapModel(Base):
    """Model of the Map table.

    ``vlr_match_id`` is the FK back to ``val_matches.vlr_match_id`` (the
    match-level numeric id, e.g. ``731406``). ``vlr_map_id`` is the
    per-map ``data-game-id`` (e.g. ``279426``), unique within ``val_maps``,
    and the column that ``val_players`` FKs against.
    """

    __tablename__ = "val_maps"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Postgres doesn't index foreign keys; Glicko loads maps per match.
    vlr_match_id: Mapped[int] = mapped_column(
        ForeignKey("val_matches.vlr_match_id"), nullable=False, index=True
    )
    vlr_map_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    map_number: Mapped[int] = mapped_column(Integer)
    map_name: Mapped[str] = mapped_column(String)
    team_1: Mapped[str] = mapped_column(String)
    team_2: Mapped[str] = mapped_column(String)
    team_1_score: Mapped[int] = mapped_column(Integer)
    team_2_score: Mapped[int] = mapped_column(Integer)
    map_winner: Mapped[str | None] = mapped_column(String, nullable=True)
    total_rounds: Mapped[int] = mapped_column(Integer)
    team_1_ct_rounds_won: Mapped[int] = mapped_column(Integer)
    team_1_t_rounds_won: Mapped[int] = mapped_column(Integer)
    team_2_ct_rounds_won: Mapped[int] = mapped_column(Integer)
    team_2_t_rounds_won: Mapped[int] = mapped_column(Integer)
    pick_team: Mapped[str | None] = mapped_column(String, nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)



