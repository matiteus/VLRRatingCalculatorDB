"""ORM model for the ``val_matches`` table representing a scraped VLR match."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from VLRRatingCalculatorDB.model.base import Base


class MatchModel(Base):
    """Model of the Match table."""

    __tablename__ = "val_matches"
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    vlr_match_id: Mapped[int] = mapped_column(Integer, unique=True)
    link: Mapped[str] = mapped_column(String)

