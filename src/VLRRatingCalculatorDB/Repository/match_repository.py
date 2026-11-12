import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as postgresql_insert
from sqlalchemy.orm import Session

from VLRRatingCalculatorDB.dto.match_info import MatchlistResponse
from VLRRatingCalculatorDB.model.match import MatchModel

class MatchRepository:

    def select_by_date_range(
        self,
        session: Session,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        statement = (
            select(
                MatchModel.vlr_match_id,
                MatchModel.match_date,
                MatchModel.has_issue,
                MatchModel.glicko_processed,
                MatchModel.glicko_error,
            )
            .where(
                MatchModel.match_date >= start_date,
                MatchModel.match_date < end_date,
            )
            .order_by(MatchModel.match_date, MatchModel.vlr_match_id)
        )
        return [dict(row) for row in session.execute(statement).mappings()]

    def get_all_matches(self, session: Session) -> list[MatchlistResponse]:
        stmt = select(MatchModel.id, MatchModel.link)
        result = session.execute(stmt).all()
        return [MatchlistResponse(id=row[0], link=row[1]) for row in result]

    def get_all_match_links(self, session: Session) -> set[str]:
        """Every stored match link; cheaper than ``get_all_matches``."""
        return set(session.scalars(select(MatchModel.link)))

    def check_if_match_exists(self, session: Session, match_link: str) -> bool:
        """Return ``True`` if a match with the given link already exists."""
        stmt = select(MatchModel.id).where(MatchModel.link == match_link).limit(1)
        return session.scalar(stmt) is not None

    def insert_match(self, match_data: dict, session: Session | None, commit: bool = True) -> dict:
        """Insert a new match row unless its ``vlr_match_id`` is already stored.

        One round trip: ``INSERT ... ON CONFLICT DO NOTHING RETURNING id``,
        instead of a separate existence check followed by an insert.

        Returns:
            A status dict. On duplicate: ``{"status": "Match already exists"}``.
            On insert: ``{"status": "Match added successfully", "match_id": <id>}``.
        """
        if session is None:
            raise ValueError("Session is None. Please provide a valid session.")

        statement = (
            postgresql_insert(MatchModel)
            .values(**match_data)
            .on_conflict_do_nothing(index_elements=[MatchModel.vlr_match_id])
            .returning(MatchModel.id)
        )
        match_id = session.scalar(statement)
        if match_id is None:
            return {"status": "Match already exists"}
        if commit:
            session.commit()
        return {"status": "Match added successfully", "match_id": match_id}
