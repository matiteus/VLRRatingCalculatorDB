"""Pydantic schemas for per-round payloads."""

from pydantic import BaseModel


class RoundInput(BaseModel):
    """Payload accepted when creating a new round row."""

    vlr_match_id: int
    vlr_map_id: int
    round_number: int
    winner: str | None = None
    winning_side: str | None = None
    win_type: str | None = None
    team_1_score: int | None = None
    team_2_score: int | None = None
