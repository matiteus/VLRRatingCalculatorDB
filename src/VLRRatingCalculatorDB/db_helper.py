"""High-level helper for engine, session, and CRUD operations."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
        self.Session = None
        self.engine = create_engine(database_url)


    def create_data_base(self) -> None:
        """Create all tables defined on ``Base.metadata`` in the target database."""
        Base.metadata.create_all(self.engine)


    def create_session(self) -> None:
        """Creates the session."""
        self.Session = sessionmaker(bind=self.engine)


    def check_if_match_exists(self, match_link:str) -> bool:
        """Return ``True`` if a match with the given link already exists."""
        match_info = self.Session.query(
            MatchModel,
        ).filter(
            MatchModel.match_link == match_link,
        ).first()

        return bool(match_info)



    def check_if_map_exists(self, match_id:int, map_id:int) -> bool:
        """Return ``True`` if a map with the given composite key already exists.

        Args:
            match_id: Foreign key to the parent match row.
            map_id: VLR-assigned id of the map within the match.

        """
        map_info = self.Session.query(
            MapModel,
        ).filter(
            MapModel.match_id == match_id,
            MapModel.map_id == map_id,
        ).first()

        return bool(map_info)


    def add_match(self, match_dict:dict) -> dict:
        """Insert a new match row, unless one with the same link already exists.

        Args:
            match_dict: Keyword arguments matching ``MatchModel`` columns
                (e.g. ``{"link": "..."}``).

        Returns:
            A status dict. On duplicate: ``{"status": "Match already exists"}``.
            On insert: ``{"status": "Match added successfully", "match_id": <id>}``.

        """
        if self._check_if_match_exists(match_dict["match_link"]):
            return {"status": "Match already exists"}
        match = MatchModel(**match_dict)
        self.Session.add(match)
        self.Session.commit()
        self.Session.refresh(match)
        return {"status": "Match added successfully", "match_id": match.id}


    def add_map(self, map_dict:dict) ->bool:
        """Insert a new map row, unless the (match_id, map_id) pair exists.

        Args:
            map_dict: Keyword arguments matching ``MapModel`` columns.

        Returns:
            A status dict. On duplicate: ``{"status": "Map already exists"}``.
            On insert: ``{"status": "Map added successfully", "map_id": <id>}``.

        """
        if self._check_if_map_exists(map_dict["match_id"], map_dict["map_id"]):
            return {"status": "Map already exists"}
        map_info = MapModel(**map_dict)
        self.Session.add(map_info)
        self.Session.commit()
        self.Session.refresh(map_info)
        return {"status": "Map added successfully", "map_id": map_info["id"]}

    def add_player(self, player_dict:dict) ->None:
        """Insert a single player stats row and return the persisted model.

        Args:
            player_dict: Keyword arguments matching ``PlayerModel`` columns.

        Returns:
            The refreshed ``PlayerModel`` instance with its assigned ``id``.

        """
        player = PlayerModel(**player_dict)
        self.Session.add(player)
        self.Session.commit()
        self.Session.refresh(player)

    def close_session(self) -> None:
        self.Session.close()

