"""ORM model for the ``val_vetoes`` table: one row per step of a map veto."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from VLRRatingCalculatorDB.model.base import Base


class VetoModel(Base):
    """Model of the Veto table.

    ``action`` is ``ban``, ``pick`` or ``remains`` (the leftover decider).
    ``team`` is the acting team's tag (NULL for ``remains``).
    """

    __tablename__ = "val_vetoes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vlr_match_id: Mapped[int] = mapped_column(
        ForeignKey("val_matches.vlr_match_id"), nullable=False, index=True
    )
    step: Mapped[int] = mapped_column(Integer, nullable=False)
    team: Mapped[str | None] = mapped_column(String, nullable=True)
    action: Mapped[str] = mapped_column(String, nullable=False)
    map_name: Mapped[str] = mapped_column(String, nullable=False)
