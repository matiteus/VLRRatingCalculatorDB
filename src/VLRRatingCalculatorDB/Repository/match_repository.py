from VLRRatingCalculatorDB.dto.match_info import MatchlistResponse
from VLRRatingCalculatorDB.model.match import MatchModel

from sqlalchemy.orm import Session
from sqlalchemy import  select

class MatchRepository:


    def get_all_matches(self, session: Session) -> list[MatchlistResponse]:
        stmt = select(MatchModel.id, MatchModel.link)
        result = session.execute(stmt).all()
        return [MatchlistResponse(id=row[0], link=row[1]) for row in result]


    def check_if_match_exists(self,session:Session, match_link: str) -> bool:
        """Return ``True`` if a match with the given link already exists."""
        stmt = (
            select(
                MatchModel.link
            ).where((
                MatchModel.link == match_link
                )
            )
        )
        match_info = session.execute(stmt).scalar_one_or_none()
        return bool(match_info)

    def insert_match(self, match_data: MatchModel, session: Session|None, commit: bool = True) ->dict:
        """Insert a new match row, unless one with the same link already exists.

        Args:
            match_data: Keyword arguments matching ``MatchModel`` columns
                (e.g. ``{"link": "..."}``).

        Returns:
            A status dict. On duplicate: ``{"status": "Match already exists"}``.
            On insert: ``{"status": "Match added successfully", "match_id": <id>}``.

        """
        if session is None:
            raise ValueError("Session is None. Please provide a valid session.")

  
        if self.check_if_match_exists(session,getattr(match_data, "link")):
            print(f"  Match already exists in database: {getattr(match_data, 'link')}")
            return {"status": "Match already exists"}
        session.add(match_data)
        if commit:
            session.commit()
        else:
            session.flush()
        session.refresh(match_data)
        
        return {"status": "Match added successfully", "match_id": match_data.id}
    



    # def fetch_repeated_links_in_list(self, match_link: list, session: Session) -> bool:
    #     """Return ``True`` if a match with the given link already exists."""
    #     stmt = (
    #         select(
    #             MatchModel.link
    #         ).where((
    #             MatchModel.link.isin_(match_link)
    #             )
    #         )
    #     )
    #     match_info = session.execute(stmt)
        
    #     return match_info
    

    # def fetch_match(self, match_link: str, session: Session) -> MatchModel:
    #     stmt = (
    #         select(
    #             MatchModel.id
    #         ).where(
    #             MatchModel.link == match_link
    #         )
    #     )

    #     match_id = session.execute(stmt)
    #     if len(match_id) == 0:
    #         raise ValueError("No match found with the given link")
    #     if len(match_id) > 1:
    #         raise ValueError("Multiple matches found with the same link")

    #     return match_id
    
