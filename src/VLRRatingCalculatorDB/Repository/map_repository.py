from VLRRatingCalculatorDB.model.map import MapModel
from VLRRatingCalculatorDB.dto.map_info import MapInput

from sqlalchemy.orm import Session
from sqlalchemy import  select

class MapRepository:


    def insert_maps(self, maps_data: list[MapInput], session: Session|None) -> dict[int, int]:
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

        map_models = [MapModel(**map_data) for map_data in maps_data]
        session.add_all(map_models)
        session.commit()
        for m in map_models:
            session.refresh(m)

        return {m.vlr_map_id: m.id for m in map_models}