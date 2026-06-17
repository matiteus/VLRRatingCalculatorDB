"""ORM model for the ``val_players`` table storing per-player stats per map."""

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from VLRRatingCalculatorDB.model.base import Base


class PlayerModel(Base):
    """Model of the Player table."""

    __tablename__ = "val_players"
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    db_match_id: Mapped[int] = mapped_column(ForeignKey("val_matches.id"))
    vlr_match_id: Mapped[int] = mapped_column(Integer)
    map_id:Mapped[int] = mapped_column(ForeignKey("val_maps.id"))
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
    kast: Mapped[float] = mapped_column(Float)
    adr: Mapped[float] = mapped_column(Float)
    hs: Mapped[String] = mapped_column(String)
    fb: Mapped[int] = mapped_column(Integer)
    fd: Mapped[int] = mapped_column(Integer)
    fk_diff: Mapped[int] = mapped_column(Integer)


