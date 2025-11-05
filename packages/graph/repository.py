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
from packages.shared.models.age import (
    parse_agtype_to_edge,
    validate_entity_properties,
    validate_relationship_properties,
    EntityProperties,
    RelationshipResult,
)
from packages.shared.models.age import parse_agtype_to_vertex

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

    async def find_entity_by_name(self, name: str) -> Optional[EntityProperties]:
        """
        Find an entity by name with runtime validation.

        Args:
            name: Entity name

        Returns:
            Validated EntityProperties or None
            
        Raises:
            AgeParseError: If entity data validation fails
        """
        safe_name = name.replace("'", "\\'")
        cypher = f"MATCH (e:Entity {{name: '{safe_name}'}}) RETURN e LIMIT 1"

        try:
            results = await self.execute_cypher(cypher)
            if not results:
                return None
            
            # results[0] is already the properties dict (extracted by execute_cypher)
            # Validate entity-specific properties directly
            entity_props = validate_entity_properties(results[0])
            
            logger.info(f"Found and validated entity: {entity_props.name} ({entity_props.type})")
            return entity_props
            
        except Exception as e:
            logger.error(f"Failed to find or validate entity {name}: {e}")
            return None

    async def get_entities_by_source(
        self, source_id: UUID, limit: int = 100
    ) -> list[EntityProperties]:
        """
        Get all entities extracted from a source with validation.

        Args:
            source_id: Source UUID
            limit: Maximum number of entities

        Returns:
            List of validated EntityProperties
            
        Raises:
            AgeParseError: If any entity fails validation
        """
        cypher = f"""
            MATCH (e:Entity)-[:EXTRACTED_FROM]->(d:Document {{id: '{source_id}'}})
            RETURN e
            LIMIT {limit}
        """

        try:
            results = await self.execute_cypher(cypher)
            validated_entities = []
            
            for result in results:
                # result is already the properties dict (extracted by execute_cypher)
                # Validate entity-specific properties directly
                entity_props = validate_entity_properties(result)
                validated_entities.append(entity_props)
            
            logger.info(f"Retrieved and validated {len(validated_entities)} entities for source {source_id}")
            return validated_entities
            
        except Exception as e:
            logger.error(f"Failed to get or validate entities for source {source_id}: {e}")
            return []

    async def get_relationships_by_source(
        self, source_id: UUID, limit: int = 100
    ) -> list[RelationshipResult]:
        """
        Get all relationships from a source with validation.

        Args:
            source_id: Source UUID
            limit: Maximum number of relationships

        Returns:
            List of validated RelationshipResult objects
            
        Raises:
            AgeParseError: If any relationship fails validation
        """
        cypher = f"""
            MATCH (e1:Entity)-[r:RELATED_TO]->(e2:Entity)
            WHERE '{source_id}' IN r.source_ids
            RETURN e1, r, e2
            LIMIT {limit}
        """

        try:
            # Use parse_results=False to get raw AGE structure
            raw_results = await self.execute_cypher(cypher, parse_results=False)
            validated_relationships = []
            
            for row in raw_results:
                row_dict = dict(row)
                
                # Parse raw AGE structures
                source_vertex = parse_agtype_to_vertex(row_dict.get('e1', ''))
                edge = parse_agtype_to_edge(row_dict.get('r', ''))
                target_vertex = parse_agtype_to_vertex(row_dict.get('e2', ''))
                
                # Create validated relationship result
                rel_result = RelationshipResult(
                    source_entity=source_vertex,
                    relationship=edge,
                    target_entity=target_vertex
                )
                
                # Validate properties to ensure data integrity
                _ = rel_result.get_source_properties()
                _ = rel_result.get_relationship_properties()
                _ = rel_result.get_target_properties()
                
                validated_relationships.append(rel_result)
            
            logger.info(f"Retrieved and validated {len(validated_relationships)} relationships for source {source_id}")
            return validated_relationships
            
        except Exception as e:
            logger.error(f"Failed to get or validate relationships for source {source_id}: {e}")
            return []

    async def get_entity_relationships_validated(
        self, entity_id: UUID, limit: int = 100
    ) -> list[RelationshipResult]:
        """
        Get relationships for a specific entity with full validation.
        
        This method demonstrates the complete validation flow for relationship queries.

        Args:
            entity_id: Entity UUID
            limit: Maximum number of relationships

        Returns:
            List of validated RelationshipResult objects
            
        Raises:
            AgeParseError: If any data fails validation
        """
        cypher = f"""
            MATCH (e1:Entity {{id: '{entity_id}'}})-[r:RELATED_TO]->(e2:Entity)
            RETURN e1, r, e2
            LIMIT {limit}
        """

        try:
            # Use parse_results=False to get raw AGE structure
            raw_results = await self.execute_cypher(cypher, parse_results=False)
            validated_relationships = []
            
            for row in raw_results:
                row_dict = dict(row)
                
                # Parse and validate all components from raw AGE data
                source_vertex = parse_agtype_to_vertex(row_dict.get('e1', ''))
                edge = parse_agtype_to_edge(row_dict.get('r', ''))
                target_vertex = parse_agtype_to_vertex(row_dict.get('e2', ''))
                
                # Create relationship result
                rel_result = RelationshipResult(
                    source_entity=source_vertex,
                    relationship=edge,
                    target_entity=target_vertex
                )
                
                # Validate all properties (will raise AgeParseError if invalid)
                source_props = rel_result.get_source_properties()
                rel_props = rel_result.get_relationship_properties()
                target_props = rel_result.get_target_properties()
                
                logger.debug(
                    f"Validated relationship: {source_props.name} "
                    f"--[{rel_props.relationship_type}]--> {target_props.name}"
                )
                
                validated_relationships.append(rel_result)
            
            logger.info(
                f"Retrieved and validated {len(validated_relationships)} "
                f"relationships for entity {entity_id}"
            )
            return validated_relationships
            
        except Exception as e:
            logger.error(f"Failed to get or validate relationships for entity {entity_id}: {e}")
            return []

