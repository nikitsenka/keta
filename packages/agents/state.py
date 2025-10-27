"""
Agent state management for KETA.
"""

from typing import Any, Optional
from uuid import UUID

from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    """
    State for KETA agents.

    This state is passed between agent nodes in LangGraph.
    """

    # Input
    query: str  # User message or task
    session_id: Optional[UUID]  # Chat session identifier
    objective_id: Optional[UUID]  # Objective context
    source_id: Optional[UUID]  # Source being processed

    # Context
    conversation_history: list[dict[str, Any]]  # Previous messages
    objective_context: Optional[dict[str, Any]]  # Objective details
    source_scope: Optional[list[UUID]]  # Limit to specific sources

    # Routing
    intent: Optional[str]  # Classified intent (extract, query)
    current_agent: Optional[str]  # Active agent type
    agent_path: list[str]  # Sequence of agents executed

    # Graph data
    entities: list[dict[str, Any]]  # Retrieved entities
    relationships: list[dict[str, Any]]  # Retrieved relationships
    documents: list[dict[str, Any]]  # Referenced documents

    # Processing
    intermediate_results: list[dict[str, Any]]  # Step-by-step data
    graph_queries: list[str]  # Executed Cypher queries

    # Output
    response: Optional[str]  # Agent response text
    sources: list[dict[str, Any]]  # Source citations
    insights: list[dict[str, Any]]  # Structured insights

    # Error handling
    errors: list[str]  # Error messages
    retry_count: int  # Number of retries

    # Extraction specific
    extraction_progress: Optional[dict[str, Any]]  # Extraction progress tracking
    chunks_processed: int  # Number of chunks processed
    total_chunks: int  # Total chunks to process
