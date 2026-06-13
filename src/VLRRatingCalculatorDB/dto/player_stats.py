"""Pydantic schemas for per-player stats payloads exchanged with the API."""

from pydantic import BaseModel


class PlayerInput(BaseModel):
    """Payload accepted by the API when creating a new player stats row."""

    match_id: int
    map_id: int
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
    kast: float
    adr: float
    hs: float
    fb: int
    fd: int
    fk_diff: int


class PlayerDTO(BaseModel):
    """Full player stats representation returned to API consumers, including its id."""

    id: int
    match_id: int
    map_id: int
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
    kast: float
    adr: float
    hs: float
    fb: int
    fd: int
    fk_diff: int


class PlayerOutput(BaseModel):
    """Wrapper for a list of :class:`PlayerDTO` responses."""

    players: list[PlayerDTO]

