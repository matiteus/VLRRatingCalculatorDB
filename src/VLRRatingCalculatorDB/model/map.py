"""ORM model for the ``val_maps`` table representing a single map within a match."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from VLRRatingCalculatorDB.model.base import Base


class MapModel(Base):
    """Model of the Map table."""

    __tablename__ = "val_maps"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    db_match_id: Mapped[int] = mapped_column(ForeignKey("val_matches.id"))
    vlr_match_id: Mapped[int] = mapped_column(Integer)
    map_id: Mapped[int] = mapped_column(Integer)
    map_name: Mapped[str] = mapped_column(String)
    team_1: Mapped[str] = mapped_column(String)
    team_2: Mapped[str] = mapped_column(String)
    team_1_score: Mapped[int] = mapped_column(Integer)
    team_2_score: Mapped[int] = mapped_column(Integer)
    map_winner: Mapped[str] = mapped_column(String)
    total_rounds: Mapped[int] = mapped_column(Integer)
    team_1_ct_rounds_won: Mapped[int] = mapped_column(Integer)
    team_1_t_rounds_won: Mapped[int] = mapped_column(Integer)
    team_2_ct_rounds_won: Mapped[int] = mapped_column(Integer)
    team_2_t_rounds_won: Mapped[int] = mapped_column(Integer)



