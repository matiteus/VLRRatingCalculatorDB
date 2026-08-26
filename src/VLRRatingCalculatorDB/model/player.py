"""ORM model for the ``val_players`` table storing per-player stats per map."""

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from VLRRatingCalculatorDB.model.base import Base


class PlayerModel(Base):
    """Model of the Player table.

    Per-map rows have ``vlr_match_id`` (FK to ``val_matches.vlr_match_id``)
    and ``vlr_map_id`` (FK to ``val_maps.vlr_map_id``) both populated.

    All-maps (series-total) rows have ``vlr_match_id`` populated and
    ``vlr_map_id`` NULL.
    """

    __tablename__ = "val_players"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vlr_match_id: Mapped[int] = mapped_column(
        ForeignKey("val_matches.vlr_match_id"), nullable=False
    )
    vlr_map_id: Mapped[int | None] = mapped_column(
        ForeignKey("val_maps.vlr_map_id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String)
    team: Mapped[str] = mapped_column(String)
    agent: Mapped[str] = mapped_column(String)
    side: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column(Float)
    acs: Mapped[int] = mapped_column(Integer)
    kills: Mapped[int] = mapped_column(Integer)
    deaths: Mapped[int] = mapped_column(Integer)
    assists: Mapped[int] = mapped_column(Integer)
    kd_diff: Mapped[int] = mapped_column(Integer)
    kast: Mapped[str] = mapped_column(String)
    adr: Mapped[float] = mapped_column(Float)
    hs: Mapped[str] = mapped_column(String)
    fb: Mapped[int] = mapped_column(Integer)
    fd: Mapped[int] = mapped_column(Integer)
    fk_diff: Mapped[int] = mapped_column(Integer)


