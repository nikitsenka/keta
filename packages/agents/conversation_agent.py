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
            # Step 1: Detect if query is temporal
            is_temporal = self._detect_temporal_query(query)
            if is_temporal:
                self._log_execution("Detected temporal query - will search for DATE entities")
                logger.debug(f"[ConversationAgent] Temporal query detected: '{query}'")

            # Step 2: Extract key terms from query for entity search
            search_terms = await self._extract_search_terms(query)
            self._log_execution(f"Extracted search terms: {search_terms}")
            logger.debug(f"[ConversationAgent] Query: '{query}' -> Search terms: {search_terms}")

            # Step 3: Search for relevant entities
            relevant_entities = []

            # Search by keywords
            for term in search_terms[:5]:  # Limit to first 5 terms
                logger.debug(f"[ConversationAgent] Searching entities for term: '{term}'")
                entities = await self.entity_search.search_by_keyword(term, limit=5)
                relevant_entities.extend(entities)

            # If temporal query, also search for DATE entities
            if is_temporal:
                logger.debug("[ConversationAgent] Searching for DATE entities")
                date_entities = await self.entity_search.search_by_type("DATE", limit=10)
                relevant_entities.extend(date_entities)
                self._log_execution(f"Found {len(date_entities)} DATE entities")

            # Deduplicate entities
            seen_ids = set()
            unique_entities = []
            for entity in relevant_entities:
                entity_id = entity.get("id")
                if entity_id and entity_id not in seen_ids:
                    seen_ids.add(entity_id)
                    unique_entities.append(entity)

            self._log_execution(f"Found {len(unique_entities)} relevant entities")
            logger.debug(f"[ConversationAgent] Found {len(unique_entities)} unique entities after deduplication")

            # Step 4: Get relationships between found entities
            relationships = []
            for entity in unique_entities[:10]:  # Limit for performance
                entity_id = UUID(entity["id"])
                logger.debug(f"[ConversationAgent] Fetching relationships for entity: {entity.get('name')} ({entity_id})")
                rels = await self.relationship_traversal.get_related_entities(
                    entity_id, max_depth=1, limit=10
                )
                relationships.extend(rels)

            self._log_execution(f"Found {len(relationships)} relationships")
            logger.debug(f"[ConversationAgent] Total relationships found: {len(relationships)}")

            # Step 5: Generate answer using LLM with graph context
            entities_context = self._format_entities(unique_entities)
            relationships_context = self._format_relationships(relationships)

            response = await self.answer_chain.ainvoke(
                {
                    "question": query,
                    "entities": entities_context,
                    "relationships": relationships_context,
                }
            )

            # Step 6: Prepare source citations
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

    def _detect_temporal_query(self, query: str) -> bool:
        """
        Detect if a query is asking about dates/times.

        Args:
            query: User query

        Returns:
            True if query is temporal, False otherwise
        """
        query_lower = query.lower()
        temporal_keywords = {
            "when",
            "date",
            "time",
            "year",
            "month",
            "day",
            "period",
            "timeline",
            "schedule",
            "released",
            "launched",
            "started",
            "ended",
            "occurred",
        }

        return any(keyword in query_lower for keyword in temporal_keywords)

    async def _extract_search_terms(self, query: str) -> list[str]:
        """
        Extract key search terms from user query.

        Args:
            query: User query

        Returns:
            List of search terms
        """
        terms = query.lower().split()

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
            relationships: List of relationship dictionaries with structure:
                {
                    'source_entity': {'id': '...', 'name': '...', 'type': '...'},
                    'relationship': {'relationship_type': '...', 'description': '...', 'confidence': ...},
                    'target_entity': {'id': '...', 'name': '...', 'type': '...'}
                }

        Returns:
            Formatted string
        """
        if not relationships:
            return "No relationships found."

        formatted = []
        for rel in relationships[:20]:
            try:
                source = rel.get("source_entity", {}).get("properties", {})
                relationship = rel.get("relationship", {}).get("properties", {})
                target = rel.get("target_entity", {}).get("properties", {})

                source_name = source.get("name", "Unknown")
                source_type = source.get("type", "Unknown")
                target_name = target.get("name", "Unknown")
                target_type = target.get("type", "Unknown")

                rel_type = relationship.get("relationship_type", "RELATED_TO")
                rel_desc = relationship.get("description", "")
                confidence = relationship.get("confidence", 0.0)

                rel_text = f"- {source_name} ({source_type}) {rel_type} {target_name} ({target_type})"
                if rel_desc:
                    rel_text += f': "{rel_desc}"'
                rel_text += f" (confidence: {confidence:.2f})"

                formatted.append(rel_text)

            except Exception as e:
                logger.warning(f"Failed to format relationship: {e}, data: {rel}")
                continue

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
