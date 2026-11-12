import datetime
from typing import Any

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from VLRRatingCalculatorDB.model.map import MapModel
from VLRRatingCalculatorDB.model.match import MatchModel
from VLRRatingCalculatorDB.dto.map_info import MapInput

class MapRepository:

    def select_by_match_date_range(
        self,
        session: Session,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        statement = (
            select(
                MapModel.vlr_match_id,
                MapModel.vlr_map_id,
                MapModel.map_number,
                MapModel.team_1,
                MapModel.team_2,
                MapModel.map_winner,
            )
            .join(MatchModel, MapModel.vlr_match_id == MatchModel.vlr_match_id)
            .where(
                MatchModel.match_date >= start_date,
                MatchModel.match_date < end_date,
            )
            .order_by(
                MatchModel.match_date,
                MapModel.vlr_match_id,
                MapModel.map_number,
            )
        )
        return [dict(row) for row in session.execute(statement).mappings()]

    def insert_maps(self, maps_data: list[MapInput], session: Session|None, commit: bool = True) -> dict[int, int]:
        """Insert a list of new map rows.

        Args:
            maps_data: List of keyword arguments matching ``MapModel`` columns
                (e.g. ``[{"vlr_match_id": 123, "link": "..."}, ...]``).

        Returns:
            A mapping ``{vlr_map_id: id}`` so callers can tag dependent rows
            (e.g. ``val_players.db_map_id``) with the freshly assigned PK.
            Empty dict on no-op / failure.

        """
        if session is None:
            raise ValueError("Session is None. Please provide a valid session.")
        if not maps_data:
            return {}

        # Bulk INSERT ... RETURNING straight from the dicts (no ORM objects).
        statement = insert(MapModel).returning(MapModel.vlr_map_id, MapModel.id)
        map_ids = dict(session.execute(statement, maps_data).tuples().all())
        if commit:
            session.commit()
        return map_ids