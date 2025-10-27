"""
Objectives repository implementation.
"""

from typing import Optional
from uuid import UUID

import asyncpg

from packages.shared.database import DatabasePool
from packages.shared.repositories.base import TableRepository


class ObjectivesRepository(TableRepository):
    """
    Repository for objectives table.
    """

    def __init__(self, db_pool: DatabasePool) -> None:
        super().__init__(db_pool, "objectives")

    async def get_by_name(self, name: str) -> Optional[asyncpg.Record]:
        """
        Get an objective by name.

        Args:
            name: Objective name

        Returns:
            Objective record or None
        """
        query = "SELECT * FROM keta.objectives WHERE name = $1"
        return await self.db_pool.fetchrow(query, name)

    async def get_stats(self, objective_id: UUID) -> Optional[asyncpg.Record]:
        """
        Get statistics for an objective.

        Args:
            objective_id: Objective UUID

        Returns:
            Statistics record or None
        """
        query = "SELECT * FROM keta.objective_stats WHERE id = $1"
        return await self.db_pool.fetchrow(query, objective_id)

    async def list_by_status(
        self, status: str, limit: int = 100, offset: int = 0
    ) -> list[asyncpg.Record]:
        """
        List objectives by status.

        Args:
            status: Objective status
            limit: Maximum number of records
            offset: Number of records to skip

        Returns:
            List of objective records
        """
        query = """
            SELECT * FROM keta.objectives
            WHERE status = $1
            ORDER BY created_at DESC
            LIMIT $2 OFFSET $3
        """
        return await self.db_pool.fetch(query, status, limit, offset)
