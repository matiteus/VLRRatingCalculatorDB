"""Pydantic schemas for match payloads exchanged with the API."""

import datetime

from pydantic import BaseModel


class MatchInput(BaseModel):
    """Payload accepted by the API when creating a new match row."""

    vlr_match_id: int
    link: str
    match_date: datetime.datetime
    has_issue: bool = False
    glicko_processed: bool = False
    glicko_error: int = 0
    event_id: int | None = None
    event_name: str | None = None
    event_stage: str | None = None
    series_format: str | None = None
    patch: str | None = None
    team_1_id: int | None = None
    team_1_name: str | None = None
    team_2_id: int | None = None
    team_2_name: str | None = None

class MatchDTO(BaseModel):
    """Full match representation returned to API consumers, including its id."""

    id: int
    vlr_match_id: int
    link: str
    match_date: datetime.datetime
    has_issue: bool
    glicko_processed: bool
    glicko_error: int
    event_id: int | None = None
    event_name: str | None = None
    event_stage: str | None = None
    series_format: str | None = None
    patch: str | None = None
    team_1_id: int | None = None
    team_1_name: str | None = None
    team_2_id: int | None = None
    team_2_name: str | None = None

class MatchOutput(BaseModel):
    """Wrapper for a list of :class:`MatchDTO` responses."""

    matches: list[MatchDTO]

class MatchlistResponse(BaseModel):
    """Response model for a list of matches with only id and link."""

    id: int
    link: str
