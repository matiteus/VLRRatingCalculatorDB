"""Pydantic schemas for map-veto payloads."""

from pydantic import BaseModel


class VetoInput(BaseModel):
    """Payload accepted when creating a new veto step row."""

    vlr_match_id: int
    step: int
    team: str | None = None
    action: str
    map_name: str
