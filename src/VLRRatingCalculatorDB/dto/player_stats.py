"""Pydantic schemas for per-player stats payloads exchanged with the API."""

from pydantic import BaseModel


class PlayerInput(BaseModel):
    """Payload accepted by the API when creating a new player stats row."""

    vlr_match_id: int
    vlr_map_id: int | None = None
    name: str
    team: str
    player_id: int | None = None
    team_id: int | None = None
    country: str | None = None
    agent: str
    side: str
    rating: float | None = None
    acs: int | None = None
    kills: int | None = None
    deaths: int | None = None
    assists: int | None = None
    kd_diff: int | None = None
    kast: str | None = None
    adr: float | None = None
    hs: str | None = None
    fb: int | None = None
    fd: int | None = None
    fk_diff: int | None = None


class PlayerDTO(BaseModel):
    """Full player stats representation returned to API consumers, including its id."""

    id: int
    vlr_match_id: int
    vlr_map_id: int | None = None
    name: str
    team: str
    player_id: int | None = None
    team_id: int | None = None
    country: str | None = None
    agent: str
    side: str
    rating: float | None = None
    acs: int | None = None
    kills: int | None = None
    deaths: int | None = None
    assists: int | None = None
    kd_diff: int | None = None
    kast: str | None = None
    adr: float | None = None
    hs: str | None = None
    fb: int | None = None
    fd: int | None = None
    fk_diff: int | None = None


class PlayerOutput(BaseModel):
    """Wrapper for a list of :class:`PlayerDTO` responses."""

    players: list[PlayerDTO]

