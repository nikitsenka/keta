"""
Graph query tools for KETA conversation agent.
"""

import logging
from typing import Any, Optional
from uuid import UUID

from packages.graph.repository import KnowledgeGraphRepository

logger = logging.getLogger(__name__)


class EntitySearchTool:
    """
    Tool for searching entities in the knowledge graph.
    """

    def __init__(self, graph_repo: KnowledgeGraphRepository) -> None:
        """
        Initialize the entity search tool.

        Args:
            graph_repo: Knowledge graph repository
        """
        self.graph_repo = graph_repo

    async def search_by_name(self, name: str) -> Optional[dict[str, Any]]:
        """
        Search for an entity by name.

        Args:
            name: Entity name

        Returns:
            Entity data or None
        """
        try:
            entity = await self.graph_repo.find_entity_by_name(name)
            if entity:
                logger.info(f"Found entity: {name}")
            return entity
        except Exception as e:
            logger.error(f"Entity search failed for '{name}': {e}")
            return None

    async def search_by_type(
        self, entity_type: str, limit: int = 10
    ) -> list[dict[str, Any]]:
        """
        Search for entities by type.

        Args:
            entity_type: Entity type (PERSON, ORGANIZATION, etc.)
            limit: Maximum number of results

        Returns:
            List of entities
        """
        cypher = f"""
            MATCH (e:Entity {{type: '{entity_type}'}})
            RETURN e
            LIMIT {limit}
        """

        try:
            logger.debug(f"[EntitySearchTool] Searching entities by type: {entity_type}, limit: {limit}")
            results = await self.graph_repo.execute_cypher(cypher)
            logger.info(f"Found {len(results)} entities of type {entity_type}")
            return results
        except Exception as e:
            logger.error(f"Entity type search failed for '{entity_type}': {e}")
            return []

    async def search_by_keyword(
        self, keyword: str, limit: int = 10
    ) -> list[dict[str, Any]]:
        """
        Search for entities containing a keyword in their name.

        Args:
            keyword: Keyword to search for
            limit: Maximum number of results

        Returns:
            List of entities
        """
        # AGE doesn't have great text search, so we'll use pattern matching
        safe_keyword = keyword.replace("'", "\\'")
        cypher = f"""
            MATCH (e:Entity)
            WHERE e.name =~ '(?i).*{safe_keyword}.*'
            RETURN e
            LIMIT {limit}
        """

        try:
            logger.debug(f"[EntitySearchTool] Searching entities by keyword: '{keyword}', limit: {limit}")
            results = await self.graph_repo.execute_cypher(cypher)
            logger.info(f"Found {len(results)} entities matching keyword '{keyword}'")
            return results
        except Exception as e:
            logger.error(f"Keyword search failed for '{keyword}': {e}")
            return []


class RelationshipTraversalTool:
    """
    Tool for traversing relationships in the knowledge graph.
    """

    def __init__(self, graph_repo: KnowledgeGraphRepository) -> None:
        """
        Initialize the relationship traversal tool.

        Args:
            graph_repo: Knowledge graph repository
        """
        self.graph_repo = graph_repo

    async def get_related_entities(
        self, entity_id: UUID, max_depth: int = 1, limit: int = 20
    ) -> list[dict[str, Any]]:
        """
        Get entities related to a given entity.

        Args:
            entity_id: Starting entity UUID
            max_depth: Maximum traversal depth
            limit: Maximum number of results

        Returns:
            List of related entities with relationship info
        """
        cypher = f"""
            MATCH (e1:Entity {{id: '{entity_id}'}})-[r]-(e2:Entity)
            RETURN {{
                source_entity: e1,
                relationship: r,
                target_entity: e2
            }}
            LIMIT {limit}
        """

        try:
            logger.debug(f"[RelationshipTraversalTool] Getting related entities for: {entity_id}, max_depth: {max_depth}, limit: {limit}")
            results = await self.graph_repo.execute_cypher(cypher)
            logger.info(f"Found {len(results)} related entities for {entity_id}")
            return results
        except Exception as e:
            logger.error(f"Relationship traversal failed for {entity_id}: {e}")
            return []

    async def get_relationships_between(
        self, entity1_id: UUID, entity2_id: UUID
    ) -> list[dict[str, Any]]:
        """
        Get relationships between two specific entities.

        Args:
            entity1_id: First entity UUID
            entity2_id: Second entity UUID

        Returns:
            List of relationships
        """
        cypher = f"""
            MATCH (e1:Entity {{id: '{entity1_id}'}})-[r]-(e2:Entity {{id: '{entity2_id}'}})
            RETURN {{
                source_entity: e1,
                relationship: r,
                target_entity: e2
            }}
        """

        try:
            results = await self.graph_repo.execute_cypher(cypher)
            logger.info(f"Found {len(results)} relationships between entities")
            return results
        except Exception as e:
            logger.error(f"Failed to get relationships between entities: {e}")
            return []

    async def get_relationship_types(
        self, entity_id: UUID
    ) -> list[dict[str, Any]]:
        """
        Get all relationship types for an entity.

        Args:
            entity_id: Entity UUID

        Returns:
            List of relationship types with counts
        """
        cypher = f"""
            MATCH (e:Entity {{id: '{entity_id}'}})-[r:RELATED_TO]-(other)
            RETURN r.relationship_type as type, count(*) as count
        """

        try:
            results = await self.graph_repo.execute_cypher(cypher)
            logger.info(f"Found {len(results)} relationship types")
            return results
        except Exception as e:
            logger.error(f"Failed to get relationship types: {e}")
            return []


class GraphQueryTool:
    """
    Tool for executing custom Cypher queries on the knowledge graph.
    """

    def __init__(self, graph_repo: KnowledgeGraphRepository) -> None:
        """
        Initialize the graph query tool.

        Args:
            graph_repo: Knowledge graph repository
        """
        self.graph_repo = graph_repo

    async def execute_query(self, cypher_query: str) -> list[dict[str, Any]]:
        """
        Execute a custom Cypher query.

        Args:
            cypher_query: Cypher query string

        Returns:
            Query results
        """
        try:
            results = await self.graph_repo.execute_cypher(cypher_query)
            logger.info(f"Query returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return []

    async def get_entity_neighborhood(
        self, entity_id: UUID, radius: int = 2
    ) -> dict[str, Any]:
        """
        Get the full neighborhood (entities and relationships) around an entity.

        Args:
            entity_id: Central entity UUID
            radius: Neighborhood radius (depth)

        Returns:
            Dictionary with entities and relationships
        """
        cypher = f"""
            MATCH path = (center:Entity {{id: '{entity_id}'}})-[*1..{radius}]-(neighbor)
            WITH collect(distinct center) + collect(distinct neighbor) as nodes,
                 [r in relationships(path) | r] as rels
            UNWIND nodes as n
            WITH collect(distinct n) as all_nodes, rels
            UNWIND rels as r
            RETURN all_nodes, collect(distinct r) as all_rels
        """

        try:
            results = await self.graph_repo.execute_cypher(cypher)
            if results:
                return {
                    "nodes": results[0].get("all_nodes", []),
                    "relationships": results[0].get("all_rels", []),
                }
            return {"nodes": [], "relationships": []}
        except Exception as e:
            logger.error(f"Failed to get entity neighborhood: {e}")
            return {"nodes": [], "relationships": []}

    async def get_shortest_path(
        self, entity1_id: UUID, entity2_id: UUID, max_depth: int = 5
    ) -> Optional[dict[str, Any]]:
        """
        Find the shortest path between two entities.

        Args:
            entity1_id: First entity UUID
            entity2_id: Second entity UUID
            max_depth: Maximum path length

        Returns:
            Path information or None
        """
        cypher = f"""
            MATCH path = shortestPath(
                (e1:Entity {{id: '{entity1_id}'}})-[*1..{max_depth}]-(e2:Entity {{id: '{entity2_id}'}})
            )
            RETURN path, length(path) as path_length
        """

        try:
            results = await self.graph_repo.execute_cypher(cypher)
            if results:
                logger.info(f"Found shortest path of length {results[0].get('path_length')}")
                return results[0]
            return None
        except Exception as e:
            logger.error(f"Failed to find shortest path: {e}")
            return None
