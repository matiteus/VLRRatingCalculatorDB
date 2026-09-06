

from sqlalchemy.orm import Session

from VLRRatingCalculatorDB.dto.player_stats import PlayerInput
from VLRRatingCalculatorDB.model.player import PlayerModel

class PlayerRepository:


    def insert_players(self, players_data: list[PlayerInput], session: Session|None, commit: bool = True) -> list[int]:
        """Insert a list of new player rows.

        Args:
            players_data: List of keyword arguments matching ``PlayerModel`` columns
                (e.g. ``[{"vlr_match_id": 123, "link": "..."}, ...]``).

        Returns:
            The list of freshly assigned ``val_players.id`` values, in insertion
            order.

        """
        if session is None:
            raise ValueError("Session is None. Please provide a valid session.")

        player_models = [PlayerModel(**player_data) for player_data in players_data]
        session.add_all(player_models)
        if commit:
            session.commit()
        else:
            session.flush()
        for p in player_models:
            session.refresh(p)

        return [p.id for p in player_models]