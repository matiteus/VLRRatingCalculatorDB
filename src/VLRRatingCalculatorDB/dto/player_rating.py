"""DTO for current and historical Glicko player ratings."""

import datetime

from pydantic import BaseModel


class PlayerRatingDTO(BaseModel):
    """One current or historical rating row."""

    id: int
    player_name: str
    team: str | None = None
    version: str
    match_id: int | None = None
    match_date: datetime.datetime | None = None
    base_rating: float
    rating_deviation: float
    volatility: float
    modifiers: dict[str, float]
    last_match_date: datetime.datetime | None = None
    matches_played: int


