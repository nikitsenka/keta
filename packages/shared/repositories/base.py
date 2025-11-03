"""
Base repository classes for KETA.
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar
from uuid import UUID

import asyncpg

from packages.shared.database import DatabasePool

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository class.
    """

    def __init__(self, db_pool: DatabasePool) -> None:
        self.db_pool = db_pool

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[T]:
        """Get a record by ID."""
        pass

    @abstractmethod
    async def create(self, data: dict[str, Any]) -> T:
        """Create a new record."""
        pass

    @abstractmethod
    async def update(self, id: UUID, data: dict[str, Any]) -> Optional[T]:
        """Update a record by ID."""
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Delete a record by ID."""
        pass


class TableRepository(BaseRepository[T], Generic[T]):
    """
    Base repository for PostgreSQL table operations.
    """

    def __init__(self, db_pool: DatabasePool, table_name: str) -> None:
        super().__init__(db_pool)
        self.table_name = table_name

    async def get_by_id(self, id: UUID) -> Optional[asyncpg.Record]:
        """
        Get a record by ID.

        Args:
            id: Record UUID

        Returns:
            Record or None if not found
        """
        query = f"SELECT * FROM keta.{self.table_name} WHERE id = $1"
        return await self.db_pool.fetchrow(query, id)

    async def get_all(
        self, limit: int = 100, offset: int = 0, order_by: str = "created_at DESC"
    ) -> list[asyncpg.Record]:
        """
        Get all records with pagination.

        Args:
            limit: Maximum number of records
            offset: Number of records to skip
            order_by: ORDER BY clause

        Returns:
            List of records
        """
        query = f"""
            SELECT * FROM keta.{self.table_name}
            ORDER BY {order_by}
            LIMIT $1 OFFSET $2
        """
        return await self.db_pool.fetch(query, limit, offset)

    async def create(self, data: dict[str, Any]) -> asyncpg.Record:
        """
        Create a new record.

        Args:
            data: Record data

        Returns:
            Created record
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(f"${i+1}" for i in range(len(data)))
        values = list(data.values())

        query = f"""
            INSERT INTO keta.{self.table_name} ({columns})
            VALUES ({placeholders})
            RETURNING *
        """
        return await self.db_pool.fetchrow(query, *values)

    async def update(self, id: UUID, data: dict[str, Any]) -> Optional[asyncpg.Record]:
        """
        Update a record by ID.

        Args:
            id: Record UUID
            data: Updated data

        Returns:
            Updated record or None if not found
        """
        if not data:
            return await self.get_by_id(id)

        set_clause = ", ".join(f"{key} = ${i+2}" for i, key in enumerate(data.keys()))
        values = [id] + list(data.values())

        query = f"""
            UPDATE keta.{self.table_name}
            SET {set_clause}
            WHERE id = $1
            RETURNING *
        """
        return await self.db_pool.fetchrow(query, *values)

    async def delete(self, id: UUID) -> bool:
        """
        Delete a record by ID.

        Args:
            id: Record UUID

        Returns:
            True if deleted, False if not found
        """
        query = f"DELETE FROM keta.{self.table_name} WHERE id = $1"
        result = await self.db_pool.execute(query, id)
        return result == "DELETE 1"

    async def count(self, where_clause: str = "", params: list = None) -> int:
        """
        Count records.

        Args:
            where_clause: Optional WHERE clause (without WHERE keyword)
            params: Query parameters

        Returns:
            Count of records
        """
        query = f"SELECT COUNT(*) FROM keta.{self.table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"

        params = params or []
        return await self.db_pool.fetchval(query, *params)

    async def exists(self, id: UUID) -> bool:
        """
        Check if a record exists.

        Args:
            id: Record UUID

        Returns:
            True if exists, False otherwise
        """
        query = f"SELECT EXISTS(SELECT 1 FROM keta.{self.table_name} WHERE id = $1)"
        return await self.db_pool.fetchval(query, id)


class GraphRepository(BaseRepository[T], Generic[T]):
    """
    Base repository for Apache AGE graph operations.
    """

    def __init__(self, db_pool: DatabasePool, graph_name: str = "keta_graph") -> None:
        super().__init__(db_pool)
        self.graph_name = graph_name

    @staticmethod
    def _parse_agtype_value(value: Any) -> Any:
        """
        Recursively parse agtype values (vertices, edges, or nested objects).

        Args:
            value: Value to parse (could be string, dict, list)

        Returns:
            Parsed value
        """
        if isinstance(value, str):
            if '::vertex' in value or '::edge' in value:
                json_str = value.replace('::vertex', '').replace('::edge', '').strip()
                try:
                    parsed = json.loads(json_str)
                    if isinstance(parsed, dict) and 'properties' in parsed:
                        return parsed['properties']
                    return parsed
                except (json.JSONDecodeError, Exception):
                    return value
            return value
        elif isinstance(value, dict):
            return {k: GraphRepository._parse_agtype_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [GraphRepository._parse_agtype_value(item) for item in value]
        return value

    @staticmethod
    def _parse_agtype(agtype_str: str) -> Optional[dict]:
        """
        Parse Apache AGE agtype format to extract properties.

        Args:
            agtype_str: Agtype string (e.g., '{...}::vertex' or '{...}::edge')

        Returns:
            Properties dict or None if parsing fails
        """
        if not agtype_str or not isinstance(agtype_str, str):
            return None

        try:
            if '::vertex' in agtype_str:
                json_str = agtype_str.replace('::vertex', '').strip()
            elif '::edge' in agtype_str:
                json_str = agtype_str.replace('::edge', '').strip()
            else:
                json_str = agtype_str.strip()

            parsed = json.loads(json_str)

            if isinstance(parsed, dict) and 'properties' in parsed:
                return parsed['properties']

            if isinstance(parsed, dict):
                return GraphRepository._parse_agtype_value(parsed)

            return parsed if isinstance(parsed, dict) else None

        except (json.JSONDecodeError, Exception):
            return None

    async def execute_cypher(self, cypher_query: str, parse_results: bool = True) -> list:
        """
        Execute a Cypher query.

        Args:
            cypher_query: Cypher query string
            parse_results: Whether to parse agtype results

        Returns:
            Query results
        """
        logger = logging.getLogger(__name__)
        logger.debug(f"[GraphRepo] Executing Cypher on graph '{self.graph_name}':\n{cypher_query}")
        
        results = await self.db_pool.execute_cypher(self.graph_name, cypher_query)
        logger.debug(f"[GraphRepo] Query returned {len(results)} raw results")
        
        if parse_results and results:
            parsed_results = []
            for row in results:
                row_dict = dict(row)

                if 'result' in row_dict:
                    properties = self._parse_agtype(row_dict['result'])
                    if properties:
                        parsed_results.append(properties)
                else:
                    parsed_results.append(row_dict)

            logger.debug(f"[GraphRepo] Parsed to {len(parsed_results)} results")
            return parsed_results
        return results

    async def get_by_id(self, id: UUID) -> Optional[T]:
        """
        Get a node by ID.

        Args:
            id: Node UUID

        Returns:
            Node or None
        """
        cypher = f"""
            MATCH (n {{id: '{id}'}})
            RETURN n
        """
        results = await self.execute_cypher(cypher)
        return results[0] if results else None

    async def create(self, data: dict[str, Any]) -> T:
        """
        Create a node (implementation specific to node type).

        Args:
            data: Node properties

        Returns:
            Created node
        """
        raise NotImplementedError("Subclasses must implement create method")

    async def update(self, id: UUID, data: dict[str, Any]) -> Optional[T]:
        """
        Update a node by ID.

        Args:
            id: Node UUID
            data: Updated properties

        Returns:
            Updated node or None
        """
        set_clause = ", ".join(f"n.{key} = '{value}'" for key, value in data.items())
        cypher = f"""
            MATCH (n {{id: '{id}'}})
            SET {set_clause}
            RETURN n
        """
        results = await self.execute_cypher(cypher)
        return results[0] if results else None

    async def delete(self, id: UUID) -> bool:
        """
        Delete a node by ID.

        Args:
            id: Node UUID

        Returns:
            True if deleted, False otherwise
        """
        cypher = f"""
            MATCH (n {{id: '{id}'}})
            DETACH DELETE n
            RETURN count(n) as deleted
        """
        results = await self.execute_cypher(cypher)
        return results[0].get("deleted", 0) > 0 if results else False
