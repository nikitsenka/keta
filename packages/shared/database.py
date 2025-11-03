"""
Database connection pooling for KETA.
"""

import json
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import asyncpg
from asyncpg import Pool

logger = logging.getLogger(__name__)


class DatabasePool:
    """
    Async connection pool manager for PostgreSQL with Apache AGE.
    """

    def __init__(self) -> None:
        self._pool: Optional[Pool] = None
        self._database_url: Optional[str] = None

    async def initialize(
        self,
        database_url: str,
        min_size: int = 5,
        max_size: int = 20,
        command_timeout: float = 60.0,
    ) -> None:
        """
        Initialize the connection pool.

        Args:
            database_url: PostgreSQL connection URL
            min_size: Minimum number of connections in the pool
            max_size: Maximum number of connections in the pool
            command_timeout: Timeout for commands in seconds
        """
        if self._pool is not None:
            logger.warning("Database pool already initialized")
            return

        self._database_url = database_url

        async def init_connection(conn):
            """Initialize connection with type codecs."""
            await self._setup_age(conn)
            await conn.set_type_codec(
                'jsonb',
                encoder=json.dumps,
                decoder=json.loads,
                schema='pg_catalog'
            )

        try:
            self._pool = await asyncpg.create_pool(
                dsn=database_url,
                min_size=min_size,
                max_size=max_size,
                command_timeout=command_timeout,
                server_settings={
                    "search_path": "keta,ag_catalog,public",
                },
                init=init_connection,
            )
            logger.info(
                f"Database pool initialized with min_size={min_size}, max_size={max_size}"
            )
            logger.info("Apache AGE extension loaded successfully")

        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise

    async def _setup_age(self, conn: asyncpg.Connection) -> None:
        """
        Set up Apache AGE extension for a connection.

        Args:
            conn: Database connection
        """
        try:
            # Load AGE extension
            await conn.execute("LOAD 'age';")
            # Set search path to include ag_catalog
            await conn.execute("SET search_path = keta, ag_catalog, public;")
        except Exception as e:
            logger.error(f"Failed to set up Apache AGE: {e}")
            raise

    async def close(self) -> None:
        """Close the connection pool."""
        if self._pool is not None:
            await self._pool.close()
            logger.info("Database pool closed")
            self._pool = None

    @asynccontextmanager
    async def acquire(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """
        Acquire a connection from the pool.

        Yields:
            Database connection

        Raises:
            RuntimeError: If pool is not initialized
        """
        if self._pool is None:
            raise RuntimeError("Database pool not initialized")

        async with self._pool.acquire() as conn:
            # Ensure AGE is loaded for this connection
            await self._setup_age(conn)
            yield conn

    async def execute(self, query: str, *args) -> str:
        """
        Execute a query without returning results.

        Args:
            query: SQL query
            *args: Query parameters

        Returns:
            Query status
        """
        async with self.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args) -> list[asyncpg.Record]:
        """
        Fetch multiple rows from a query.

        Args:
            query: SQL query
            *args: Query parameters

        Returns:
            List of records
        """
        async with self.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args) -> Optional[asyncpg.Record]:
        """
        Fetch a single row from a query.

        Args:
            query: SQL query
            *args: Query parameters

        Returns:
            Single record or None
        """
        async with self.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query: str, *args, column: int = 0):
        """
        Fetch a single value from a query.

        Args:
            query: SQL query
            *args: Query parameters
            column: Column index to return

        Returns:
            Single value
        """
        async with self.acquire() as conn:
            return await conn.fetchval(query, *args, column=column)

    async def execute_cypher(self, graph_name: str, cypher_query: str) -> list[asyncpg.Record]:
        """
        Execute an Apache AGE Cypher query.

        Args:
            graph_name: Name of the graph
            cypher_query: Cypher query

        Returns:
            Query results
        """
        # AGE requires queries to be wrapped in the cypher function
        query = f"SELECT * FROM cypher('{graph_name}', $$ {cypher_query} $$) as (result agtype);"
        logger.debug(f"[DB] Executing Cypher query on graph '{graph_name}':\n{cypher_query}")
        logger.debug(f"[DB] Full SQL query:\n{query}")
        return await self.fetch(query)

    @property
    def is_initialized(self) -> bool:
        """Check if the pool is initialized."""
        return self._pool is not None


# Global database pool instance
db_pool = DatabasePool()


async def get_db_pool() -> DatabasePool:
    """
    Dependency for getting the database pool.

    Returns:
        Database pool instance
    """
    if not db_pool.is_initialized:
        raise RuntimeError("Database pool not initialized")
    return db_pool
