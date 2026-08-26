"""Pydantic schemas for per-player stats payloads exchanged with the API."""

from pydantic import BaseModel


class PlayerInput(BaseModel):
    """Payload accepted by the API when creating a new player stats row."""

    vlr_match_id: int
    vlr_map_id: int | None = None
    name: str
    team: str
    agent: str
    side: str
    rating: float
    acs: int
    kills: int
    deaths: int
    assists: int
    kd_diff: int
    kast: str
    adr: float
    hs: str
    fb: int
    fd: int
    fk_diff: int


class PlayerDTO(BaseModel):
    """Full player stats representation returned to API consumers, including its id."""

    id: int
    vlr_match_id: int
    vlr_map_id: int | None = None
    name: str
    team: str
    agent: str
    side: str
    rating: float
    acs: int
    kills: int
    deaths: int
    assists: int
    kd_diff: int
    kast: str
    adr: float
    hs: str
    fb: int
    fd: int
    fk_diff: int


class PlayerOutput(BaseModel):
    """Wrapper for a list of :class:`PlayerDTO` responses."""

    players: list[PlayerDTO]

