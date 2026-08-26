"""Pydantic schemas for match payloads exchanged with the API."""

import datetime

from pydantic import BaseModel


class MatchInput(BaseModel):
    """Payload accepted by the API when creating a new match row."""

    vlr_match_id: int
    link: str
    match_date: datetime.datetime
    has_issue: bool = False

class MatchDTO(BaseModel):
    """Full match representation returned to API consumers, including its id."""

    id: int
    vlr_match_id: int
    link: str
    match_date: datetime.datetime
    has_issue: bool

class MatchOutput(BaseModel):
    """Wrapper for a list of :class:`MatchDTO` responses."""

    matches: list[MatchDTO]

class MatchlistResponse(BaseModel):
    """Response model for a list of matches with only id and link."""

    id: int
    link: str
