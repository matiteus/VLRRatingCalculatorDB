"""High-level helper for engine, session, and CRUD operations."""

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from VLRRatingCalculatorDB.dto.player_stats import PlayerInput
from VLRRatingCalculatorDB.model.base import Base
from VLRRatingCalculatorDB.model.match import MatchModel



from VLRRatingCalculatorDB.Repository.match_repository import MatchRepository
from VLRRatingCalculatorDB.Repository.map_repository import MapRepository
from VLRRatingCalculatorDB.Repository.player_repository import PlayerRepository

from VLRRatingCalculatorDB.dto.match_info import MatchlistResponse
from VLRRatingCalculatorDB.dto.map_info import MapInput

class DBHelper:
    """Database access layer backed by SQLAlchemy.

    Wraps engine creation, schema setup, session management, and the
    common add/exists checks used by the VLR scrapper pipeline.
    """
    match_repository = MatchRepository()
    map_repository = MapRepository()
    player_repository = PlayerRepository()
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

    def insert_match(self, match_data: dict):
        match = MatchModel(**match_data)
        return self.match_repository.insert_match(match, self.session)

    def insert_maps(self, maps_data: list[MapInput]):
        return self.map_repository.insert_maps(maps_data, self.session)

    def insert_players(self, players_data: list[PlayerInput]):
        return self.player_repository.insert_players(players_data, self.session)


    def check_if_match_exists(self, match_link: str) -> bool:
        """Return ``True`` if a match with the given link already exists."""
        if self.session is None:
            raise ValueError("Session is None. Please create a session first.")
        return self.match_repository.check_if_match_exists(self.session, match_link)

    def get_all_matches(self) -> list[MatchlistResponse]:
        """Return a list of all matches in the database."""
        if self.session is None:
            raise ValueError("Session is None. Please create a session first.")
        return self.match_repository.get_all_matches(self.session)



