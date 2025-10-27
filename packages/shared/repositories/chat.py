"""
Chat sessions and messages repository implementation.
"""

from typing import Optional
from uuid import UUID

import asyncpg

from packages.shared.database import DatabasePool
from packages.shared.repositories.base import TableRepository


class ChatSessionsRepository(TableRepository):
    """
    Repository for chat_sessions table.
    """

    def __init__(self, db_pool: DatabasePool) -> None:
        super().__init__(db_pool, "chat_sessions")

    async def get_by_objective(
        self, objective_id: UUID, limit: int = 100, offset: int = 0
    ) -> list[asyncpg.Record]:
        """
        Get all sessions for an objective.

        Args:
            objective_id: Objective UUID
            limit: Maximum number of records
            offset: Number of records to skip

        Returns:
            List of session records
        """
        query = """
            SELECT * FROM keta.chat_sessions
            WHERE objective_id = $1 AND status = 'ACTIVE'
            ORDER BY last_message_at DESC NULLS LAST, created_at DESC
            LIMIT $2 OFFSET $3
        """
        return await self.db_pool.fetch(query, objective_id, limit, offset)

    async def update_last_message_time(self, session_id: UUID) -> None:
        """
        Update the last_message_at timestamp for a session.

        Args:
            session_id: Session UUID
        """
        query = """
            UPDATE keta.chat_sessions
            SET last_message_at = NOW()
            WHERE id = $1
        """
        await self.db_pool.execute(query, session_id)


class ChatMessagesRepository(TableRepository):
    """
    Repository for chat_messages table.
    """

    def __init__(self, db_pool: DatabasePool) -> None:
        super().__init__(db_pool, "chat_messages")

    async def get_by_session(
        self,
        session_id: UUID,
        limit: int = 100,
        offset: int = 0,
        include_deleted: bool = False,
    ) -> list[asyncpg.Record]:
        """
        Get all messages for a session.

        Args:
            session_id: Session UUID
            limit: Maximum number of records
            offset: Number of records to skip
            include_deleted: Include soft-deleted messages

        Returns:
            List of message records
        """
        if include_deleted:
            where_clause = "WHERE session_id = $1"
        else:
            where_clause = "WHERE session_id = $1 AND deleted_at IS NULL"

        query = f"""
            SELECT * FROM keta.chat_messages
            {where_clause}
            ORDER BY created_at ASC
            LIMIT $2 OFFSET $3
        """
        return await self.db_pool.fetch(query, session_id, limit, offset)

    async def soft_delete(self, message_id: UUID) -> bool:
        """
        Soft delete a message.

        Args:
            message_id: Message UUID

        Returns:
            True if deleted, False otherwise
        """
        query = """
            UPDATE keta.chat_messages
            SET deleted_at = NOW()
            WHERE id = $1 AND deleted_at IS NULL
            RETURNING id
        """
        result = await self.db_pool.fetchrow(query, message_id)
        return result is not None

    async def get_conversation_history(
        self, session_id: UUID, limit: int = 10
    ) -> list[dict[str, str]]:
        """
        Get recent conversation history formatted for LLM context.

        Args:
            session_id: Session UUID
            limit: Number of recent messages

        Returns:
            List of messages formatted for LLM
        """
        query = """
            SELECT role, content, created_at
            FROM keta.chat_messages
            WHERE session_id = $1 AND deleted_at IS NULL
            ORDER BY created_at DESC
            LIMIT $2
        """
        records = await self.db_pool.fetch(query, session_id, limit)

        # Reverse to get chronological order
        history = []
        for record in reversed(records):
            history.append({"role": record["role"], "content": record["content"]})

        return history
