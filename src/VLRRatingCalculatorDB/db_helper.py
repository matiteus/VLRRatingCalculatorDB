"""High-level helper for engine, session, and CRUD operations."""

import datetime
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from VLRRatingCalculatorDB.dto.agent_info import AgentInput
from VLRRatingCalculatorDB.dto.map_info import MapInput
from VLRRatingCalculatorDB.dto.match_info import MatchlistResponse
from VLRRatingCalculatorDB.dto.player_stats import PlayerInput
from VLRRatingCalculatorDB.dto.prediction_info import PredictionInput
from VLRRatingCalculatorDB.dto.round_info import RoundInput
from VLRRatingCalculatorDB.dto.veto_info import VetoInput
from VLRRatingCalculatorDB.model.base import Base
from VLRRatingCalculatorDB.Repository.agent_repository import AgentRepository
from VLRRatingCalculatorDB.Repository.map_repository import MapRepository
from VLRRatingCalculatorDB.Repository.match_repository import MatchRepository
from VLRRatingCalculatorDB.Repository.player_rating_repository import PlayerRatingRepository
from VLRRatingCalculatorDB.Repository.player_repository import PlayerRepository
from VLRRatingCalculatorDB.Repository.prediction_repository import PredictionRepository
from VLRRatingCalculatorDB.Repository.round_repository import RoundRepository
from VLRRatingCalculatorDB.Repository.veto_repository import VetoRepository


class DBHelper:
    """Database access layer backed by SQLAlchemy.

    Wraps engine creation, schema setup, session management, and the
    common add/exists checks used by the VLR scrapper pipeline.
    """

    match_repository = MatchRepository()
    map_repository = MapRepository()
    player_repository = PlayerRepository()
    player_rating_repository = PlayerRatingRepository()
    agent_repository = AgentRepository()
    prediction_repository = PredictionRepository()
    round_repository = RoundRepository()
    veto_repository = VetoRepository()

    def __init__(
        self,
        database_url: str,
        engine_options: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the helper with a SQLAlchemy engine bound to ``database_url``."""
        self.session: Session | None = None
        self.engine = create_engine(database_url, **(engine_options or {}))

    # Schema and session
    ##################################################################
    def create_data_base(self) -> None:
        """Create all tables (and their indexes) that don't exist yet."""
        Base.metadata.create_all(self.engine)

    def create_agents_table(self) -> None:
        """Create only the agents table if it does not already exist."""
        self.agent_repository.create_table(self.engine)

    def create_predictions_table(self) -> None:
        """Create only the predictions table if it does not already exist."""
        self.prediction_repository.create_table(self.engine)

    def create_session(self) -> None:
        """Create a new ``Session`` instance bound to the engine."""
        self.session = sessionmaker(bind=self.engine)()

    def close_session(self) -> None:
        """Close the active session, if one exists."""
        if self.session is not None:
            self.session.close()
            self.session = None

    def _require_session(self) -> Session:
        if self.session is None:
            raise ValueError("Session is None. Please create a session first.")
        return self.session

    # Inserts
    ##################################################################
    def insert_match_bundle(
        self,
        match_data: dict,
        maps_data: list[MapInput],
        players_data: list[PlayerInput],
        rounds_data: list[RoundInput] | None = None,
        vetoes_data: list[VetoInput] | None = None,
    ) -> dict:
        """Insert one match and all dependent rows in one transaction.

        Returns the ``insert_match`` status dict; nothing else is written
        when the match is already stored.
        """
        session = self._require_session()
        try:
            match_result = self.match_repository.insert_match(match_data, session, commit=False)
            if "match_id" not in match_result:
                session.rollback()
                return match_result
            # Maps before players and rounds: both reference val_maps.
            self.map_repository.insert_maps(maps_data, session, commit=False)
            self.player_repository.insert_players(players_data, session, commit=False)
            self.round_repository.insert_rounds(rounds_data or [], session, commit=False)
            self.veto_repository.insert_vetoes(vetoes_data or [], session, commit=False)
            session.commit()
            return match_result
        except Exception:
            session.rollback()
            raise

    def insert_match(self, match_data: dict) -> dict:
        return self.match_repository.insert_match(match_data, self._require_session())

    def insert_maps(self, maps_data: list[MapInput]):
        return self.map_repository.insert_maps(maps_data, self._require_session())

    def insert_players(self, players_data: list[PlayerInput]):
        return self.player_repository.insert_players(players_data, self._require_session())

    def insert_agents(self, agents_data: list[AgentInput]):
        """Insert agents and return their database IDs.

        Existing agent names are returned without being inserted again.
        """
        return self.agent_repository.insert_agents(agents_data, self._require_session())

    def insert_predictions(
        self,
        predictions_data: list[PredictionInput],
        commit: bool = True,
    ) -> int:
        """Save or update prediction rows through the prediction repository."""
        return self.prediction_repository.insert_predictions(
            predictions_data, self._require_session(), commit=commit
        )

    # Reads
    ##################################################################
    def check_if_match_exists(self, match_link: str) -> bool:
        """Return ``True`` if a match with the given link already exists."""
        return self.match_repository.check_if_match_exists(self._require_session(), match_link)

    def get_all_matches(self) -> list[MatchlistResponse]:
        """Return a list of all matches in the database."""
        return self.match_repository.get_all_matches(self._require_session())

    def get_all_match_links(self) -> set[str]:
        """Return every stored match link (what the scraper needs to skip known matches)."""
        return self.match_repository.get_all_match_links(self._require_session())

    def select_player(
        self,
        vlr_match_id: int | None = None,
        vlr_map_id: int | None = None,
        name: str | None = None,
        columns: list[str] | None = None,
        vlr_match_ids: list[int] | None = None,
        vlr_map_ids: list[int] | None = None,
        vlr_match_map_ids: list[tuple[int, int]] | None = None,
        vlr_match_map_names: list[tuple[int, int, str]] | None = None,
        vlr_match_map_name_sides: list[tuple[int, int, str, str]] | None = None,
    ):
        """Select player rows through the player repository."""
        return self.player_repository.select_player(
            self._require_session(),
            vlr_match_id=vlr_match_id,
            vlr_map_id=vlr_map_id,
            name=name,
            columns=columns,
            vlr_match_ids=vlr_match_ids,
            vlr_map_ids=vlr_map_ids,
            vlr_match_map_ids=vlr_match_map_ids,
            vlr_match_map_names=vlr_match_map_names,
            vlr_match_map_name_sides=vlr_match_map_name_sides,
        )

    def select_matches_by_date_range(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        """Return match metadata in the half-open date range [start, end)."""
        return self.match_repository.select_by_date_range(
            self._require_session(), start_date, end_date
        )

    def select_maps_by_match_date_range(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        """Return maps belonging to matches in the half-open date range."""
        return self.map_repository.select_by_match_date_range(
            self._require_session(), start_date, end_date
        )

    def select_series_player_stats_by_match_date_range(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        """Return series-total player statistics in the half-open date range."""
        return self.player_repository.select_series_totals_by_match_date_range(
            self._require_session(), start_date, end_date
        )

    def select_rating_snapshots_by_date_range(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        """Return player rating snapshots in the half-open date range [start, end)."""
        return self.player_rating_repository.select_by_date_range(
            self._require_session(), start_date, end_date
        )
