"""Pydantic schemas for map payloads exchanged with the API."""

from pydantic import BaseModel


class MapInput(BaseModel):
    """Payload accepted by the API when creating a new map row."""

    match_id: int
    map_id: int
    map_name: str
    team_1: str
    team_2: str
    team_1_score: int
    team_2_score: int
    map_winner: str
    total_rounds: int
    team_1_ct_rounds_won: int
    team_1_t_rounds_won: int
    team_2_ct_rounds_won: int
    team_2_t_rounds_won: int

class MapDTO(BaseModel):
    """Full map representation returned to API consumers, including its id."""

    id: int
    match_id: int
    map_id: int
    map_name: str
    team_1: str
    team_2: str
    team_1_score: int
    team_2_score: int
    map_winner: str
    total_rounds: int
    team_1_ct_rounds_won: int
    team_1_t_rounds_won: int
    team_2_ct_rounds_won: int
    team_2_t_rounds_won: int

class MapOutput(BaseModel):
    """Wrapper for a list of :class:`MapDTO` responses."""

    maps: list[MapDTO]

