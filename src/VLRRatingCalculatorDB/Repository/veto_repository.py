from sqlalchemy.orm import Session

from VLRRatingCalculatorDB.dto.veto_info import VetoInput
from VLRRatingCalculatorDB.model.veto import VetoModel


class VetoRepository:

    def insert_vetoes(self, vetoes_data: list[VetoInput], session: Session | None, commit: bool = True) -> int:
        """Bulk-insert veto rows (dicts matching ``VetoModel`` columns); return how many."""
        if session is None:
            raise ValueError("Session is None. Please provide a valid session.")
        if vetoes_data:
            session.execute(VetoModel.__table__.insert(), vetoes_data)
        if commit:
            session.commit()
        return len(vetoes_data)
