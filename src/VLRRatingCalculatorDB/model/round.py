"""ORM model for the ``val_rounds`` table: one row per played round of a map."""

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from VLRRatingCalculatorDB.model.base import Base


class RoundModel(Base):
    """Model of the Round table.

    ``winner`` is the winning team's tag, matching ``val_maps.team_1`` /
    ``team_2``. ``win_type`` is how the round ended: ``elim``, ``boom``
    (spike exploded), ``defuse`` or ``time``. ``team_1_score`` /
    ``team_2_score`` are the map score after this round.
    """

    __tablename__ = "val_rounds"
    __table_args__ = (
        UniqueConstraint("vlr_map_id", "round_number", name="uq_val_rounds_map_round"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vlr_match_id: Mapped[int] = mapped_column(
        ForeignKey("val_matches.vlr_match_id"), nullable=False, index=True
    )
    vlr_map_id: Mapped[int] = mapped_column(ForeignKey("val_maps.vlr_map_id"), nullable=False)
    round_number: Mapped[int] = mapped_column(Integer, nullable=False)
    winner: Mapped[str | None] = mapped_column(String, nullable=True)
    winning_side: Mapped[str | None] = mapped_column(String, nullable=True)
    win_type: Mapped[str | None] = mapped_column(String, nullable=True)
    team_1_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    team_2_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
