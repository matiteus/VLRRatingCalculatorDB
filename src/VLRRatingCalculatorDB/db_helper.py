"""High-level helper for engine, session, and CRUD operations."""

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from VLRRatingCalculatorDB.model.base import Base
from VLRRatingCalculatorDB.model.map import MapModel
from VLRRatingCalculatorDB.model.match import MatchModel
from VLRRatingCalculatorDB.model.player import PlayerModel


class DBHelper:
    """Database access layer backed by SQLAlchemy.

    Wraps engine creation, schema setup, session management, and the
    common add/exists checks used by the VLR scrapper pipeline.
    """

    def __init__(self, database_url: str) -> None:
        """Initialize the helper with a SQLAlchemy engine bound to ``database_url``."""
        self.session: Session | None = None
        self.engine = create_engine(database_url)


    def create_data_base(self) -> None:
        """Create all tables defined on ``Base.metadata`` in the target database."""
        Base.metadata.create_all(self.engine)


    def create_session(self) -> None:
        """Create a new ``Session`` instance bound to the engine."""
        self.session = sessionmaker(bind=self.engine)()


    def check_if_match_exists(self, match_link: str) -> bool:
        """Return ``True`` if a match with the given link already exists."""
        stmt = (
            select(
                MatchModel.link
            ).where((
                MatchModel.link == match_link
                )
            )
        )
        match_info = self.session.execute(stmt).scalar_one_or_none()
        return bool(match_info)


    def get_match_id(self, match_link: str) -> int | None:
        """Return the primary key of the match with the given link, or ``None``.

        Use this to resolve a VLR match link to the internal ``val_matches.id``
        that foreign keys (e.g. ``val_maps.match_id``) need to point at.
        """
        stmt = select(MatchModel.id).where(MatchModel.link == match_link)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_map_id(self, match_id: int, map_id: int) -> int | None:
        """Return the primary key of the map with the given composite key, or ``None``."""
        stmt = select(MapModel.id).where(
            MapModel.val_match_id == match_id,
            MapModel.map_id == map_id,
        )
        return self.session.execute(stmt).scalar_one_or_none()


    def check_if_map_exists(self, match_id: int, map_id: int) -> bool:
        """Return ``True`` if a map with the given composite key already exists.

        Args:
            match_id: Foreign key to the parent match row.
            map_id: VLR-assigned id of the map within the match.

        """
        stmt = (
            select(
                MapModel.map_id,
                MapModel.match_id
            ).where(
                MapModel.match_id == match_id,
                MapModel.map_id == map_id,
            )  
        )
        map_info = self.session.execute(stmt).scalar_one_or_none()

        return bool(map_info)


    def add_match(self, match_dict: dict) -> dict:
        """Insert a new match row, unless one with the same link already exists.

        Args:
            match_dict: Keyword arguments matching ``MatchModel`` columns
                (e.g. ``{"link": "..."}``).

        Returns:
            A status dict. On duplicate: ``{"status": "Match already exists"}``.
            On insert: ``{"status": "Match added successfully", "match_id": <id>}``.

        """
        if self.check_if_match_exists(match_dict["link"]):
            return {"status": "Match already exists"}
        match = MatchModel(**match_dict)
        self.session.add(match)
        self.session.commit()
        self.session.refresh(match)
        return {"status": "Match added successfully", "match_id": match.id}


    def add_map(self, map_dict: dict) -> dict:
        """Insert a new map row, unless the (match_id, map_id) pair exists.

        Args:
            map_dict: Keyword arguments matching ``MapModel`` columns.

        Returns:
            A status dict. On duplicate: ``{"status": "Map already exists"}``.
            On insert: ``{"status": "Map added successfully", "map_id": <id>}``.

        """
        if self.check_if_map_exists(map_dict["vlr_match_id"], map_dict["map_id"]):
            return {"status": "Map already exists"}
        map_info = MapModel(**map_dict)
        self.session.add(map_info)
        self.session.commit()
        self.session.refresh(map_info)
        return {"status": "Map added successfully", "map_id": map_info.id}


    def add_player(self, player_dict: dict) -> None:
        """Insert a single player stats row and persist it.

        Args:
            player_dict: Keyword arguments matching ``PlayerModel`` columns.

        """
        player = PlayerModel(**player_dict)
        self.session.add(player)
        self.session.commit()
        self.session.refresh(player)


    def close_session(self) -> None:
        """Close the active session, if one is open."""
        if self.session is not None:
            self.session.close()

