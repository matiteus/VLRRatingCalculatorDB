"""ORM model for the ``val_players`` table storing per-player stats per map."""

from sqlalchemy import Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from VLRRatingCalculatorDB.model.base import Base


class PlayerModel(Base):
    """Model of the Player table.

    Per-map rows have ``vlr_match_id`` (FK to ``val_matches.vlr_match_id``)
    and ``vlr_map_id`` (FK to ``val_maps.vlr_map_id``) both populated.

    All-maps (series-total) rows have ``vlr_match_id`` populated and
    ``vlr_map_id`` NULL.

    Stat columns are NULL when vlr.gg had no value for that player/side.
    ``player_id`` / ``team_id`` are vlr.gg's stable ids (names and tags
    change); NULL for rows scraped before they were extracted.
    """

    __tablename__ = "val_players"
    __table_args__ = (
        Index(
            "ix_val_players_match_map_name_side",
            "vlr_match_id",
            "vlr_map_id",
            "name",
            "side",
        ),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vlr_match_id: Mapped[int] = mapped_column(
        ForeignKey("val_matches.vlr_match_id"), nullable=False
    )
    vlr_map_id: Mapped[int | None] = mapped_column(
        ForeignKey("val_maps.vlr_map_id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String)
    team: Mapped[str] = mapped_column(String)
    player_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    team_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    agent: Mapped[str | None] = mapped_column(String, nullable=True)
    side: Mapped[str] = mapped_column(String)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    acs: Mapped[int | None] = mapped_column(Integer, nullable=True)
    kills: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deaths: Mapped[int | None] = mapped_column(Integer, nullable=True)
    assists: Mapped[int | None] = mapped_column(Integer, nullable=True)
    kd_diff: Mapped[int | None] = mapped_column(Integer, nullable=True)
    kast: Mapped[str | None] = mapped_column(String, nullable=True)
    adr: Mapped[float | None] = mapped_column(Float, nullable=True)
    hs: Mapped[str | None] = mapped_column(String, nullable=True)
    fb: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fd: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fk_diff: Mapped[int | None] = mapped_column(Integer, nullable=True)


