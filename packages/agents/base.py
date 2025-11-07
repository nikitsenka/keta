"""
Base agent class for KETA.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

from langchain_core.language_models import BaseChatModel

from packages.agents.state import AgentState
from packages.shared.config import get_settings
from packages.shared.database import DatabasePool
from packages.shared.llm_factory import create_llm

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for KETA agents.
    """

    def __init__(
        self,
        name: str,
        db_pool: DatabasePool,
        llm: Optional[BaseChatModel] = None,
    ) -> None:
        """
        Initialize the agent.

        Args:
            name: Agent name
            db_pool: Database connection pool
            llm: Language model (optional, will create default if not provided)
        """
        self.name = name
        self.db_pool = db_pool
        self.settings = get_settings()

        if llm is None:
            self.llm = create_llm(self.settings)
        else:
            self.llm = llm

        logger.info(
            f"Initialized {self.name} agent with LLM provider: {self.settings.llm_provider.value}"
        )

    @abstractmethod
    async def execute(self, state: AgentState) -> AgentState:
        """
        Execute the agent's main logic.

        Args:
            state: Current agent state

        Returns:
            Updated agent state
        """
        pass

    def _update_agent_path(self, state: AgentState) -> AgentState:
        """
        Update the agent path in state.

        Args:
            state: Current state

        Returns:
            Updated state
        """
        if "agent_path" not in state:
            state["agent_path"] = []
        state["agent_path"].append(self.name)
        state["current_agent"] = self.name
        return state

    def _add_error(self, state: AgentState, error: str) -> AgentState:
        """
        Add an error message to state.

        Args:
            state: Current state
            error: Error message

        Returns:
            Updated state
        """
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(f"[{self.name}] {error}")
        logger.error(f"{self.name}: {error}")
        return state

    def _log_execution(self, message: str) -> None:
        """
        Log agent execution message.

        Args:
            message: Log message
        """
        logger.info(f"[{self.name}] {message}")
