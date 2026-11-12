from sqlalchemy.orm import Session

from VLRRatingCalculatorDB.dto.round_info import RoundInput
from VLRRatingCalculatorDB.model.round import RoundModel


class RoundRepository:

    def insert_rounds(self, rounds_data: list[RoundInput], session: Session | None, commit: bool = True) -> int:
        """Bulk-insert round rows (dicts matching ``RoundModel`` columns); return how many."""
        if session is None:
            raise ValueError("Session is None. Please provide a valid session.")
        if rounds_data:
            session.execute(RoundModel.__table__.insert(), rounds_data)
        if commit:
            session.commit()
        return len(rounds_data)
