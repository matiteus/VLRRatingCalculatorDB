"""Pydantic schemas for match payloads exchanged with the API."""

from pydantic import BaseModel


class MatchInput(BaseModel):
    """Payload accepted by the API when creating a new match row."""

    vlr_match_id: int
    link: str

class MatchDTO(BaseModel):
    """Full match representation returned to API consumers, including its id."""

    id: int
    vlr_match_id :int
    link: str

class MatchOutput(BaseModel):
    """Wrapper for a list of :class:`MatchDTO` responses."""

    matches: list[MatchDTO]
