"""
Sources repository implementation.
"""

from typing import Optional
from uuid import UUID

import asyncpg

from packages.shared.database import DatabasePool
from packages.shared.repositories.base import TableRepository


class SourcesRepository(TableRepository):
    """
    Repository for sources table.
    """

    def __init__(self, db_pool: DatabasePool) -> None:
        super().__init__(db_pool, "sources")

    async def get_by_objective(
        self, objective_id: UUID, limit: int = 100, offset: int = 0
    ) -> list[asyncpg.Record]:
        """
        Get all sources for an objective.

        Args:
            objective_id: Objective UUID
            limit: Maximum number of records
            offset: Number of records to skip

        Returns:
            List of source records
        """
        query = """
            SELECT * FROM keta.sources
            WHERE objective_id = $1
            ORDER BY uploaded_at DESC
            LIMIT $2 OFFSET $3
        """
        return await self.db_pool.fetch(query, objective_id, limit, offset)

    async def get_by_extraction_status(
        self, status: str, limit: int = 100, offset: int = 0
    ) -> list[asyncpg.Record]:
        """
        Get sources by extraction status.

        Args:
            status: Extraction status
            limit: Maximum number of records
            offset: Number of records to skip

        Returns:
            List of source records
        """
        query = """
            SELECT * FROM keta.sources
            WHERE extraction_status = $1
            ORDER BY uploaded_at DESC
            LIMIT $2 OFFSET $3
        """
        return await self.db_pool.fetch(query, status, limit, offset)

    async def update_extraction_status(
        self,
        source_id: UUID,
        status: str,
        progress: Optional[dict] = None,
        error: Optional[str] = None,
    ) -> Optional[asyncpg.Record]:
        """
        Update extraction status for a source.

        Args:
            source_id: Source UUID
            status: New extraction status
            progress: Extraction progress data
            error: Error message if failed

        Returns:
            Updated source record or None
        """
        from datetime import datetime

        updates = {"extraction_status": status}

        if progress is not None:
            updates["extraction_progress"] = progress

        if error is not None:
            updates["extraction_error"] = error

        if status == "COMPLETED":
            updates["processed_at"] = datetime.utcnow()

        return await self.update(source_id, updates)

    async def get_by_objective_and_name(
        self, objective_id: UUID, name: str
    ) -> Optional[asyncpg.Record]:
        """
        Get a source by objective ID and name.

        Args:
            objective_id: Objective UUID
            name: Source name

        Returns:
            Source record or None
        """
        query = """
            SELECT * FROM keta.sources
            WHERE objective_id = $1 AND name = $2
        """
        return await self.db_pool.fetchrow(query, objective_id, name)
