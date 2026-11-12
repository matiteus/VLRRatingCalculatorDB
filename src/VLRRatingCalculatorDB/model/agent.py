"""ORM model for the Valorant agent catalogue."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from VLRRatingCalculatorDB.model.base import Base


class AgentModel(Base):
    """An agent and its broad competitive role."""

    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agent_name: Mapped[str] = mapped_column("agentName", String, unique=True, nullable=False)
    agent_role: Mapped[str] = mapped_column("agentRole", String, nullable=False)