from src.VLRRatingCalculatorDB.Repository.match_repository import MatchRepository
from sqlalchemy.orm import Session

class MatchService:
    match_repository = MatchRepository()

    def check_if_match_exists(self, session: Session, match_link: str) -> bool:
        return self.match_repository.check_if_match_exists(session, match_link)

    

    def add_one_match(self, match_dict, session):
        return self.match_repository.add_match(match_dict, session)
        
    # def add_many_matches(self, match_list:list,session:Session):
    #     links = []
    #     for match in match_list:
    #         links.append(match['link'])
    #     result = self.match_repository.fetch_repeated_links_in_list(links,session)
    #     print(result)

        

        
        