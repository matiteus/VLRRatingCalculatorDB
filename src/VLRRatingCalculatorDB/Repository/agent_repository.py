"""Persistence methods for Valorant agents."""

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from VLRRatingCalculatorDB.dto.agent_info import AgentInput
from VLRRatingCalculatorDB.model.base import Base
from VLRRatingCalculatorDB.model.agent import AgentModel


class AgentRepository:
    """Insert agents without creating duplicates by name."""

    def create_table(self, engine: Engine) -> None:
        """Create the agents table when it does not already exist."""
        agent_table = Base.metadata.tables[AgentModel.__tablename__]
        Base.metadata.create_all(engine, tables=[agent_table])

    def insert_agents(
        self,
        agents_data: list[AgentInput],
        session: Session | None,
        commit: bool = True,
    ) -> list[int]:
        if session is None:
            raise ValueError("Session is None. Please provide a valid session.")

        inserted_ids: list[int] = []
        for agent_data in agents_data:
            existing = session.execute(
                select(AgentModel).where(
                    AgentModel.agent_name == agent_data.agent_name
                )
            ).scalar_one_or_none()
            if existing is not None:
                inserted_ids.append(existing.id)
                continue
            agent = AgentModel(
                agent_name=agent_data.agent_name,
                agent_role=agent_data.agent_role,
            )
            session.add(agent)
            session.flush()
            inserted_ids.append(agent.id)

        if commit:
            session.commit()
        return inserted_ids