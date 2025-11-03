"""
Knowledge graph repository for KETA.
"""

import json
import logging
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from packages.shared.database import DatabasePool
from packages.shared.repositories.base import GraphRepository

logger = logging.getLogger(__name__)


class KnowledgeGraphRepository(GraphRepository):
    """
    Repository for knowledge graph operations using Apache AGE.
    """

    def __init__(self, db_pool: DatabasePool, graph_name: str = "keta_graph") -> None:
        super().__init__(db_pool, graph_name)

    async def create_entity(
        self,
        entity_id: UUID,
        name: str,
        entity_type: str,
        source_ids: list[UUID],
        confidence: float,
        extraction_method: str = "llm_structured",
    ) -> dict[str, Any]:
        """
        Create an Entity node in the graph.

        Args:
            entity_id: Unique entity identifier
            name: Entity name
            entity_type: Entity type (PERSON, ORGANIZATION, etc.)
            source_ids: List of source UUIDs
            confidence: Extraction confidence
            extraction_method: Method used for extraction

        Returns:
            Created entity data
        """
        now = datetime.utcnow().isoformat()

        # Escape single quotes in name for Cypher
        safe_name = name.replace("'", "\\'")

        cypher = f"""
            CREATE (e:Entity {{
                id: '{entity_id}',
                name: '{safe_name}',
                type: '{entity_type}',
                source_ids: {json.dumps([str(sid) for sid in source_ids])},
                confidence: {confidence},
                extraction_method: '{extraction_method}',
                created_at: '{now}',
                updated_at: '{now}'
            }})
            RETURN e
        """

        try:
            await self.execute_cypher(cypher, parse_results=False)
            logger.info(f"Created entity: {name} ({entity_type})")
            return {
                "id": str(entity_id),
                "name": name,
                "type": entity_type,
                "confidence": confidence,
            }
        except Exception as e:
            logger.error(f"Failed to create entity {name}: {e}")
            raise

    async def create_document(
        self,
        doc_id: UUID,
        title: str,
        chunk_index: int = 0,
        text_snippet: str = "",
    ) -> dict[str, Any]:
        """
        Create a Document node in the graph.

        Args:
            doc_id: Document UUID (references sources.id)
            title: Document title
            chunk_index: Chunk number
            text_snippet: Text snippet (first 500 chars)

        Returns:
            Created document data
        """
        now = datetime.utcnow().isoformat()
        safe_title = title.replace("'", "\\'")
        safe_snippet = text_snippet[:500].replace("'", "\\'")

        cypher = f"""
            MERGE (d:Document {{id: '{doc_id}', chunk_index: {chunk_index}}})
            SET d.title = '{safe_title}',
                d.text_snippet = '{safe_snippet}',
                d.created_at = '{now}'
            RETURN d
        """

        try:
            await self.execute_cypher(cypher, parse_results=False)
            logger.info(f"Created/merged document: {title} (chunk {chunk_index})")
            return {"id": str(doc_id), "title": title, "chunk_index": chunk_index}
        except Exception as e:
            logger.error(f"Failed to create document {title}: {e}")
            raise

    async def create_relationship(
        self,
        entity1_id: UUID,
        entity2_id: UUID,
        relationship_type: str,
        description: str,
        source_ids: list[UUID],
        confidence: float,
    ) -> dict[str, Any]:
        """
        Create a RELATED_TO relationship between two entities.

        Args:
            entity1_id: First entity UUID
            entity2_id: Second entity UUID
            relationship_type: Type of relationship
            description: Description of the relationship
            source_ids: List of source UUIDs
            confidence: Relationship confidence

        Returns:
            Created relationship data
        """
        safe_desc = description.replace("'", "\\'")

        cypher = f"""
            MATCH (e1:Entity {{id: '{entity1_id}'}}), (e2:Entity {{id: '{entity2_id}'}})
            CREATE (e1)-[r:RELATED_TO {{
                relationship_type: '{relationship_type}',
                description: '{safe_desc}',
                confidence: {confidence},
                source_ids: {json.dumps([str(sid) for sid in source_ids])}
            }}]->(e2)
            RETURN r
        """

        try:
            await self.execute_cypher(cypher, parse_results=False)
            logger.info(f"Created relationship: {relationship_type} ({confidence})")
            return {
                "entity1_id": str(entity1_id),
                "entity2_id": str(entity2_id),
                "relationship_type": relationship_type,
                "confidence": confidence,
            }
        except Exception as e:
            logger.error(f"Failed to create relationship {relationship_type}: {e}")
            raise

    async def link_entity_to_document(
        self,
        entity_id: UUID,
        doc_id: UUID,
        chunk_index: int = 0,
        mention_count: int = 1,
    ) -> None:
        """
        Create a MENTIONED_IN relationship between entity and document.

        Args:
            entity_id: Entity UUID
            doc_id: Document UUID
            chunk_index: Document chunk index
            mention_count: Number of mentions
        """
        cypher = f"""
            MATCH (e:Entity {{id: '{entity_id}'}}), (d:Document {{id: '{doc_id}', chunk_index: {chunk_index}}})
            CREATE (e)-[:MENTIONED_IN {{
                mention_count: {mention_count},
                positions: [],
                context_snippets: []
            }}]->(d)
        """

        try:
            await self.execute_cypher(cypher, parse_results=False)
        except Exception as e:
            logger.warning(f"Failed to link entity to document: {e}")

    async def link_entity_to_source(
        self,
        entity_id: UUID,
        doc_id: UUID,
        chunk_index: int = 0,
        confidence: float = 1.0,
        extraction_method: str = "llm_structured",
    ) -> None:
        """
        Create an EXTRACTED_FROM relationship for provenance tracking.

        Args:
            entity_id: Entity UUID
            doc_id: Document UUID
            chunk_index: Document chunk index
            confidence: Extraction confidence
            extraction_method: Method used for extraction
        """
        now = datetime.utcnow().isoformat()

        cypher = f"""
            MATCH (e:Entity {{id: '{entity_id}'}}), (d:Document {{id: '{doc_id}', chunk_index: {chunk_index}}})
            CREATE (e)-[:EXTRACTED_FROM {{
                extraction_date: '{now}',
                confidence: {confidence},
                extraction_method: '{extraction_method}'
            }}]->(d)
        """

        try:
            await self.execute_cypher(cypher, parse_results=False)
        except Exception as e:
            logger.warning(f"Failed to link entity to source: {e}")

    async def find_entity_by_name(self, name: str) -> Optional[dict[str, Any]]:
        """
        Find an entity by name.

        Args:
            name: Entity name

        Returns:
            Entity data or None
        """
        safe_name = name.replace("'", "\\'")
        cypher = f"MATCH (e:Entity {{name: '{safe_name}'}}) RETURN e LIMIT 1"

        try:
            results = await self.execute_cypher(cypher)
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Failed to find entity {name}: {e}")
            return None

    async def get_entities_by_source(
        self, source_id: UUID, limit: int = 100
    ) -> list[dict[str, Any]]:
        """
        Get all entities extracted from a source.

        Args:
            source_id: Source UUID
            limit: Maximum number of entities

        Returns:
            List of entities
        """
        cypher = f"""
            MATCH (e:Entity)-[:EXTRACTED_FROM]->(d:Document {{id: '{source_id}'}})
            RETURN e
            LIMIT {limit}
        """

        try:
            return await self.execute_cypher(cypher)
        except Exception as e:
            logger.error(f"Failed to get entities for source {source_id}: {e}")
            return []

    async def get_relationships_by_source(
        self, source_id: UUID, limit: int = 100
    ) -> list[dict[str, Any]]:
        """
        Get all relationships from a source.

        Args:
            source_id: Source UUID
            limit: Maximum number of relationships

        Returns:
            List of relationships
        """
        cypher = f"""
            MATCH (e1:Entity)-[r:RELATED_TO]->(e2:Entity)
            WHERE '{source_id}' IN r.source_ids
            RETURN e1, r, e2
            LIMIT {limit}
        """

        try:
            return await self.execute_cypher(cypher)
        except Exception as e:
            logger.error(f"Failed to get relationships for source {source_id}: {e}")
            return []
