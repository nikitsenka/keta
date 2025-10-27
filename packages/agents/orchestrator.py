"""
Agent orchestrator for KETA using LangGraph.
"""

import logging
from typing import Any, Literal

from langgraph.graph import END, StateGraph

from packages.agents.extraction_agent import ExtractionAgent
from packages.agents.state import AgentState
from packages.shared.database import DatabasePool

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Orchestrator for routing and managing KETA agents using LangGraph.
    """

    def __init__(self, db_pool: DatabasePool) -> None:
        """
        Initialize the orchestrator.

        Args:
            db_pool: Database connection pool
        """
        self.db_pool = db_pool

        # Initialize agents (import here to avoid circular imports)
        from packages.agents.conversation_agent import ConversationAgent

        self.extraction_agent = ExtractionAgent(db_pool)
        self.conversation_agent = ConversationAgent(db_pool)

        # Build the graph
        self.graph = self._build_graph()

        logger.info("Agent orchestrator initialized")

    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph state graph.

        Returns:
            Compiled state graph
        """
        # Create graph
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("classify_intent", self._classify_intent)
        workflow.add_node("extraction", self._run_extraction)
        workflow.add_node("conversation", self._run_conversation)

        # Set entry point
        workflow.set_entry_point("classify_intent")

        # Add edges
        workflow.add_conditional_edges(
            "classify_intent",
            self._route_to_agent,
            {
                "extraction": "extraction",
                "conversation": "conversation",
                "end": END,
            },
        )

        workflow.add_edge("extraction", END)
        workflow.add_edge("conversation", END)

        # Compile graph
        return workflow.compile()

    async def _classify_intent(self, state: AgentState) -> AgentState:
        """
        Classify user intent to route to appropriate agent.

        Args:
            state: Current state

        Returns:
            Updated state with intent
        """
        # Simple intent classification based on state
        # In POC, intent is determined by presence of source_id vs session_id

        if state.get("source_id"):
            state["intent"] = "extract"
            logger.info("Intent classified as: extract")
        elif state.get("session_id"):
            state["intent"] = "query"
            logger.info("Intent classified as: query")
        else:
            state["intent"] = "unknown"
            logger.warning("Could not classify intent")

        return state

    def _route_to_agent(self, state: AgentState) -> Literal["extraction", "conversation", "end"]:
        """
        Route to appropriate agent based on intent.

        Args:
            state: Current state

        Returns:
            Agent name to route to
        """
        intent = state.get("intent", "unknown")

        if intent == "extract":
            return "extraction"
        elif intent == "query":
            return "conversation"
        else:
            return "end"

    async def _run_extraction(self, state: AgentState) -> AgentState:
        """
        Run the extraction agent.

        Args:
            state: Current state

        Returns:
            Updated state
        """
        logger.info("Running extraction agent")
        return await self.extraction_agent.execute(state)

    async def _run_conversation(self, state: AgentState) -> AgentState:
        """
        Run the conversation agent.

        Args:
            state: Current state

        Returns:
            Updated state
        """
        logger.info("Running conversation agent")
        return await self.conversation_agent.execute(state)

    async def execute(self, initial_state: AgentState) -> AgentState:
        """
        Execute the agent workflow.

        Args:
            initial_state: Initial state

        Returns:
            Final state after execution
        """
        logger.info("Starting agent orchestration")

        try:
            # Run the graph
            final_state = await self.graph.ainvoke(initial_state)
            logger.info(f"Orchestration completed. Agent path: {final_state.get('agent_path', [])}")
            return final_state

        except Exception as e:
            logger.error(f"Orchestration failed: {e}", exc_info=True)
            initial_state["errors"] = initial_state.get("errors", []) + [
                f"Orchestration failed: {e}"
            ]
            return initial_state
