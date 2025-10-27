"""
Extraction Agent for KETA.
"""

import logging
from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from packages.agents.base import BaseAgent
from packages.agents.state import AgentState
from packages.agents.tools.extraction import EntityExtractor, RelationshipExtractor
from packages.graph.repository import KnowledgeGraphRepository
from packages.shared.database import DatabasePool
from packages.shared.repositories.sources import SourcesRepository
from packages.shared.text_processing import chunk_text_iterator, extract_text_snippet

logger = logging.getLogger(__name__)


class ExtractionAgent(BaseAgent):
    """
    Agent for extracting entities and relationships from text documents.
    """

    def __init__(self, db_pool: DatabasePool) -> None:
        """
        Initialize the extraction agent.

        Args:
            db_pool: Database connection pool
        """
        super().__init__(name="ExtractionAgent", db_pool=db_pool)

        # Initialize tools
        self.entity_extractor = EntityExtractor(self.llm)
        self.relationship_extractor = RelationshipExtractor(self.llm)

        # Initialize repositories
        self.sources_repo = SourcesRepository(db_pool)
        self.graph_repo = KnowledgeGraphRepository(db_pool, self.settings.graph_name)

        logger.info("ExtractionAgent initialized with entity and relationship extractors")

    async def execute(self, state: AgentState) -> AgentState:
        """
        Execute extraction on a source document.

        Args:
            state: Agent state with source_id

        Returns:
            Updated state with extraction results
        """
        self._update_agent_path(state)
        self._log_execution("Starting document extraction")

        # Get source_id from state
        source_id = state.get("source_id")
        if not source_id:
            return self._add_error(state, "No source_id provided")

        try:
            # Load source
            source = await self.sources_repo.get_by_id(source_id)
            if not source:
                return self._add_error(state, f"Source {source_id} not found")

            # Update status to PROCESSING
            await self.sources_repo.update_extraction_status(
                source_id,
                "PROCESSING",
                {
                    "current_stage": "chunking",
                    "total_chunks": 0,
                    "processed_chunks": 0,
                    "entities_extracted": 0,
                    "relationships_extracted": 0,
                },
            )

            # Extract content
            content = source["content"]
            source_name = source["name"]

            # Chunk the document
            chunks = list(
                chunk_text_iterator(content, self.settings.max_chunk_size, overlap=500)
            )
            total_chunks = len(chunks)

            self._log_execution(f"Split document into {total_chunks} chunks")

            # Update progress
            await self.sources_repo.update_extraction_status(
                source_id,
                "PROCESSING",
                {
                    "current_stage": "extracting_entities",
                    "total_chunks": total_chunks,
                    "processed_chunks": 0,
                    "entities_extracted": 0,
                    "relationships_extracted": 0,
                },
            )

            # Create document node in graph
            snippet = extract_text_snippet(content, 500)
            await self.graph_repo.create_document(
                doc_id=source_id,
                title=source_name,
                chunk_index=0,  # Simplified for POC - treat as single doc
                text_snippet=snippet,
            )

            # Track all entities and relationships
            all_entities = []
            all_relationships = []
            entity_name_to_id = {}  # Map entity names to IDs for relationship creation

            # Process each chunk
            for chunk_index, chunk_text in chunks:
                self._log_execution(f"Processing chunk {chunk_index + 1}/{total_chunks}")

                # Extract entities from chunk
                entities = await self.entity_extractor.extract(chunk_text)

                # Store entities in graph
                for entity in entities:
                    # Check if entity already exists (by name)
                    existing = await self.graph_repo.find_entity_by_name(entity["name"])

                    if existing:
                        entity_id = UUID(existing["id"])
                        logger.info(f"Entity '{entity['name']}' already exists")
                    else:
                        # Create new entity
                        entity_id = UUID(entity["id"])
                        await self.graph_repo.create_entity(
                            entity_id=entity_id,
                            name=entity["name"],
                            entity_type=entity["type"],
                            source_ids=[source_id],
                            confidence=entity["confidence"],
                            extraction_method=entity["extraction_method"],
                        )

                        # Link to document
                        await self.graph_repo.link_entity_to_document(
                            entity_id=entity_id,
                            doc_id=source_id,
                            chunk_index=0,
                            mention_count=1,
                        )

                        # Link to source for provenance
                        await self.graph_repo.link_entity_to_source(
                            entity_id=entity_id,
                            doc_id=source_id,
                            chunk_index=0,
                            confidence=entity["confidence"],
                            extraction_method=entity["extraction_method"],
                        )

                    # Track for relationship extraction
                    entity_name_to_id[entity["name"]] = entity_id
                    all_entities.append(entity)

                # Extract relationships from chunk
                if len(entities) >= 2:
                    relationships = await self.relationship_extractor.extract(
                        chunk_text, entities
                    )

                    # Store relationships in graph
                    for rel in relationships:
                        entity1_name = rel["entity1_name"]
                        entity2_name = rel["entity2_name"]

                        # Get entity IDs
                        entity1_id = entity_name_to_id.get(entity1_name)
                        entity2_id = entity_name_to_id.get(entity2_name)

                        if entity1_id and entity2_id:
                            await self.graph_repo.create_relationship(
                                entity1_id=entity1_id,
                                entity2_id=entity2_id,
                                relationship_type=rel["relationship_type"],
                                description=rel["description"],
                                source_ids=[source_id],
                                confidence=rel["confidence"],
                            )
                            all_relationships.append(rel)

                # Update progress
                await self.sources_repo.update_extraction_status(
                    source_id,
                    "PROCESSING",
                    {
                        "current_stage": "extracting_entities",
                        "total_chunks": total_chunks,
                        "processed_chunks": chunk_index + 1,
                        "entities_extracted": len(all_entities),
                        "relationships_extracted": len(all_relationships),
                    },
                )

            # Mark as completed
            await self.sources_repo.update_extraction_status(
                source_id,
                "COMPLETED",
                {
                    "current_stage": "completed",
                    "total_chunks": total_chunks,
                    "processed_chunks": total_chunks,
                    "entities_extracted": len(all_entities),
                    "relationships_extracted": len(all_relationships),
                },
            )

            # Update state
            state["entities"] = all_entities
            state["relationships"] = all_relationships
            state["response"] = (
                f"Extraction completed: {len(all_entities)} entities, "
                f"{len(all_relationships)} relationships extracted"
            )

            self._log_execution("Extraction completed successfully")
            return state

        except Exception as e:
            logger.error(f"Extraction failed: {e}", exc_info=True)

            # Update status to FAILED
            await self.sources_repo.update_extraction_status(
                source_id, "FAILED", error=str(e)
            )

            return self._add_error(state, f"Extraction failed: {e}")
