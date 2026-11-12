import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from VLRRatingCalculatorDB.model.player_rating import PlayerRatingModel


class PlayerRatingRepository:
    def select_by_date_range(
        self,
        session: Session,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        statement = (
            select(
                PlayerRatingModel.id,
                PlayerRatingModel.name,
                PlayerRatingModel.team,
                PlayerRatingModel.match_date,
                PlayerRatingModel.base_rating,
                PlayerRatingModel.rating_deviation,
                PlayerRatingModel.matches_played,
            )
            .where(
                PlayerRatingModel.match_date >= start_date,
                PlayerRatingModel.match_date < end_date,
            )
            .order_by(
                PlayerRatingModel.name,
                PlayerRatingModel.match_date,
                PlayerRatingModel.id,
            )
        )
        return [dict(row) for row in session.execute(statement).mappings()]