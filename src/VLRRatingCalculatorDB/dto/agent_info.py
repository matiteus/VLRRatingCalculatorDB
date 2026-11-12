"""Pydantic DTOs for Valorant agents."""

from pydantic import BaseModel


class AgentInput(BaseModel):
    """Agent data accepted by the database helper."""

    agent_name: str
    agent_role: str


class AgentDTO(AgentInput):
    """Agent data returned from the database."""

    id: int


class AgentOutput(BaseModel):
    """Wrapper for a list of agents."""

    agents: list[AgentDTO]