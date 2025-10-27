"""
Conversation Agent for KETA.
"""

import logging
from typing import Any
from uuid import UUID

from langchain_core.prompts import ChatPromptTemplate

from packages.agents.base import BaseAgent
from packages.agents.state import AgentState
from packages.agents.tools.graph_tools import (
    EntitySearchTool,
    GraphQueryTool,
    RelationshipTraversalTool,
)
from packages.graph.repository import KnowledgeGraphRepository
from packages.shared.database import DatabasePool

logger = logging.getLogger(__name__)


class ConversationAgent(BaseAgent):
    """
    Agent for answering questions using the knowledge graph.
    """

    def __init__(self, db_pool: DatabasePool) -> None:
        """
        Initialize the conversation agent.

        Args:
            db_pool: Database connection pool
        """
        super().__init__(name="ConversationAgent", db_pool=db_pool)

        # Initialize graph repository and tools
        self.graph_repo = KnowledgeGraphRepository(db_pool, self.settings.graph_name)
        self.entity_search = EntitySearchTool(self.graph_repo)
        self.relationship_traversal = RelationshipTraversalTool(self.graph_repo)
        self.graph_query = GraphQueryTool(self.graph_repo)

        # Create prompt template for answer generation
        self.answer_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a knowledgeable assistant that answers questions using information from a knowledge graph.

You have access to entities and their relationships extracted from documents. Use this information to provide accurate, well-sourced answers.

When answering:
- Be concise and direct
- Cite specific entities and relationships from the knowledge graph
- If information is not in the graph, say so clearly
- Provide confidence levels when appropriate

Available entities: {entities}
Available relationships: {relationships}""",
                ),
                ("human", "{question}"),
            ]
        )

        self.answer_chain = self.answer_prompt | self.llm

        logger.info("ConversationAgent initialized with graph query tools")

    async def execute(self, state: AgentState) -> AgentState:
        """
        Execute conversation to answer a user question.

        Args:
            state: Agent state with query and session context

        Returns:
            Updated state with response and sources
        """
        self._update_agent_path(state)
        self._log_execution("Starting conversation")

        # Get query from state
        query = state.get("query", "")
        if not query:
            return self._add_error(state, "No query provided")

        try:
            # Step 1: Extract key terms from query for entity search
            search_terms = await self._extract_search_terms(query)
            self._log_execution(f"Extracted search terms: {search_terms}")

            # Step 2: Search for relevant entities
            relevant_entities = []
            for term in search_terms[:5]:  # Limit to first 5 terms
                entities = await self.entity_search.search_by_keyword(term, limit=5)
                relevant_entities.extend(entities)

            # Deduplicate entities
            seen_ids = set()
            unique_entities = []
            for entity in relevant_entities:
                entity_id = entity.get("id")
                if entity_id and entity_id not in seen_ids:
                    seen_ids.add(entity_id)
                    unique_entities.append(entity)

            self._log_execution(f"Found {len(unique_entities)} relevant entities")

            # Step 3: Get relationships between found entities
            relationships = []
            for entity in unique_entities[:10]:  # Limit for performance
                entity_id = UUID(entity["id"])
                rels = await self.relationship_traversal.get_related_entities(
                    entity_id, max_depth=1, limit=10
                )
                relationships.extend(rels)

            self._log_execution(f"Found {len(relationships)} relationships")

            # Step 4: Generate answer using LLM with graph context
            entities_context = self._format_entities(unique_entities)
            relationships_context = self._format_relationships(relationships)

            response = await self.answer_chain.ainvoke(
                {
                    "question": query,
                    "entities": entities_context,
                    "relationships": relationships_context,
                }
            )

            # Step 5: Prepare source citations
            sources = self._extract_sources(unique_entities)

            # Update state
            state["entities"] = unique_entities
            state["relationships"] = relationships
            state["response"] = response.content
            state["sources"] = sources

            self._log_execution("Conversation completed successfully")
            return state

        except Exception as e:
            logger.error(f"Conversation failed: {e}", exc_info=True)
            return self._add_error(state, f"Conversation failed: {e}")

    async def _extract_search_terms(self, query: str) -> list[str]:
        """
        Extract key search terms from user query.

        Args:
            query: User query

        Returns:
            List of search terms
        """
        # Simple implementation: split on spaces and filter
        # In production, use NER or more sophisticated term extraction
        terms = query.lower().split()

        # Filter out common stop words
        stop_words = {
            "what",
            "when",
            "where",
            "who",
            "how",
            "is",
            "are",
            "was",
            "were",
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "about",
        }

        filtered_terms = [term for term in terms if term not in stop_words and len(term) > 2]

        return filtered_terms

    def _format_entities(self, entities: list[dict[str, Any]]) -> str:
        """
        Format entities for LLM context.

        Args:
            entities: List of entity dictionaries

        Returns:
            Formatted string
        """
        if not entities:
            return "No entities found."

        formatted = []
        for entity in entities[:20]:  # Limit to 20 for context size
            name = entity.get("name", "Unknown")
            entity_type = entity.get("type", "Unknown")
            confidence = entity.get("confidence", 0.0)
            formatted.append(f"- {name} ({entity_type}, confidence: {confidence:.2f})")

        return "\n".join(formatted)

    def _format_relationships(self, relationships: list[dict[str, Any]]) -> str:
        """
        Format relationships for LLM context.

        Args:
            relationships: List of relationship dictionaries

        Returns:
            Formatted string
        """
        if not relationships:
            return "No relationships found."

        formatted = []
        for rel in relationships[:20]:  # Limit to 20
            # Try to extract entity and relationship info
            # Format depends on query results structure
            formatted.append(f"- Relationship: {rel}")

        return "\n".join(formatted)

    def _extract_sources(self, entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Extract source citations from entities.

        Args:
            entities: List of entities

        Returns:
            List of source citations
        """
        sources = []
        seen_sources = set()

        for entity in entities:
            source_ids = entity.get("source_ids", [])
            for source_id in source_ids:
                if source_id not in seen_sources:
                    seen_sources.add(source_id)
                    sources.append(
                        {
                            "source_id": source_id,
                            "source_name": f"Document {source_id}",  # Would fetch actual name in production
                            "snippet": f"Entity: {entity.get('name', 'Unknown')}",
                            "relevance_score": entity.get("confidence", 0.0),
                        }
                    )

        return sources
