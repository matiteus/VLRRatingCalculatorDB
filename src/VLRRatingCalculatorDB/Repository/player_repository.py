import datetime
from typing import Any

from sqlalchemy import select, tuple_
from sqlalchemy.orm import Session

from VLRRatingCalculatorDB.dto.player_stats import PlayerInput
from VLRRatingCalculatorDB.model.match import MatchModel
from VLRRatingCalculatorDB.model.player import PlayerModel

class PlayerRepository:

    def select_series_totals_by_match_date_range(
        self,
        session: Session,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        """Return one ``both`` player-stat row per player and series."""
        statement = (
            select(
                PlayerModel.vlr_match_id,
                PlayerModel.vlr_map_id,
                PlayerModel.name,
                PlayerModel.team,
                PlayerModel.side,
                PlayerModel.rating,
                PlayerModel.acs,
                PlayerModel.kills,
                PlayerModel.deaths,
                PlayerModel.assists,
                PlayerModel.kd_diff,
                PlayerModel.kast,
                PlayerModel.adr,
                PlayerModel.hs,
                PlayerModel.fb,
                PlayerModel.fd,
                PlayerModel.fk_diff,
                MatchModel.match_date,
            )
            .join(MatchModel, PlayerModel.vlr_match_id == MatchModel.vlr_match_id)
            .where(
                MatchModel.match_date >= start_date,
                MatchModel.match_date < end_date,
                PlayerModel.vlr_map_id.is_(None),
                PlayerModel.side == "both",
            )
            .order_by(
                MatchModel.match_date,
                PlayerModel.vlr_match_id,
                PlayerModel.name,
            )
        )
        return [dict(row) for row in session.execute(statement).mappings()]


    def insert_players(self, players_data: list[PlayerInput], session: Session|None, commit: bool = True) -> int:
        """Bulk-insert player rows; return how many were inserted.

        Args:
            players_data: List of dicts matching ``PlayerModel`` columns.

        Plain Core ``executemany``: no ORM objects and no ``RETURNING``.
        Players are ~80% of the rows in a match, and this was the slowest
        part of saving one (17.7 -> 9.1 ms for 180 rows in a benchmark).
        """
        if session is None:
            raise ValueError("Session is None. Please provide a valid session.")
        if players_data:
            session.execute(PlayerModel.__table__.insert(), players_data)
        if commit:
            session.commit()
        return len(players_data)

    def select_player(
        self,
        session: Session | None,
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
        """Select player rows, optionally filtered or limited to columns."""
        if session is None:
            raise ValueError("Session is None. Please provide a valid session.")

        if columns is None:
            statement = select(PlayerModel)
        else:
            invalid_columns = set(columns) - set(PlayerModel.__table__.columns.keys())
            if invalid_columns:
                raise ValueError(f"Unknown player columns: {sorted(invalid_columns)}")
            selected_columns = [getattr(PlayerModel, column) for column in columns]
            statement = select(*selected_columns)

        if vlr_match_id is not None:
            statement = statement.where(PlayerModel.vlr_match_id == vlr_match_id)
        if vlr_map_id is not None:
            statement = statement.where(PlayerModel.vlr_map_id == vlr_map_id)
        if name is not None:
            statement = statement.where(PlayerModel.name == name)
        if vlr_match_ids is not None:
            statement = statement.where(PlayerModel.vlr_match_id.in_(vlr_match_ids))
        if vlr_map_ids is not None:
            statement = statement.where(PlayerModel.vlr_map_id.in_(vlr_map_ids))
        if vlr_match_map_ids is not None:
            statement = statement.where(
                tuple_(PlayerModel.vlr_match_id, PlayerModel.vlr_map_id).in_(
                    vlr_match_map_ids
                )
            )
        if vlr_match_map_names is not None:
            statement = statement.where(
                tuple_(
                    PlayerModel.vlr_match_id,
                    PlayerModel.vlr_map_id,
                    PlayerModel.name,
                ).in_(vlr_match_map_names)
            )
        if vlr_match_map_name_sides is not None:
            statement = statement.where(
                tuple_(
                    PlayerModel.vlr_match_id,
                    PlayerModel.vlr_map_id,
                    PlayerModel.name,
                    PlayerModel.side,
                ).in_(vlr_match_map_name_sides)
            )

        if columns is not None:
            return list(session.execute(statement).mappings().all())
        return list(session.scalars(statement).all())