"""
Chat session and message endpoints.
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from packages.agents.orchestrator import AgentOrchestrator
from packages.agents.state import AgentState
from packages.shared.database import DatabasePool, get_db_pool
from packages.shared.models import (
    ChatSessionCreate,
    ChatSessionResponse,
    MessageCreate,
    MessageResponse,
    SourceCitation,
)
from packages.shared.repositories import ObjectivesRepository
from packages.shared.repositories.chat import ChatMessagesRepository, ChatSessionsRepository

logger = logging.getLogger(__name__)

router = APIRouter()


def get_chat_sessions_repo(
    db_pool: DatabasePool = Depends(get_db_pool),
) -> ChatSessionsRepository:
    """Dependency for getting chat sessions repository."""
    return ChatSessionsRepository(db_pool)


def get_chat_messages_repo(
    db_pool: DatabasePool = Depends(get_db_pool),
) -> ChatMessagesRepository:
    """Dependency for getting chat messages repository."""
    return ChatMessagesRepository(db_pool)


def get_objectives_repo(
    db_pool: DatabasePool = Depends(get_db_pool),
) -> ObjectivesRepository:
    """Dependency for getting objectives repository."""
    return ObjectivesRepository(db_pool)


def get_orchestrator(
    db_pool: DatabasePool = Depends(get_db_pool),
) -> AgentOrchestrator:
    """Dependency for getting agent orchestrator."""
    return AgentOrchestrator(db_pool)


@router.post("/chat/sessions", response_model=ChatSessionResponse, status_code=201)
async def create_chat_session(
    session: ChatSessionCreate,
    sessions_repo: ChatSessionsRepository = Depends(get_chat_sessions_repo),
    objectives_repo: ObjectivesRepository = Depends(get_objectives_repo),
) -> ChatSessionResponse:
    """Create a new chat session."""
    try:
        # Verify objective exists
        objective = await objectives_repo.get_by_id(session.objective_id)
        if not objective:
            raise HTTPException(status_code=404, detail="Objective not found")

        # Create session
        data = session.model_dump()
        data["status"] = "ACTIVE"
        record = await sessions_repo.create(data)

        return ChatSessionResponse(**dict(record))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create chat session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create chat session")


@router.get("/chat/sessions", response_model=list[ChatSessionResponse])
async def list_chat_sessions(
    objective_id: UUID = Query(...),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    sessions_repo: ChatSessionsRepository = Depends(get_chat_sessions_repo),
) -> list[ChatSessionResponse]:
    """List chat sessions for an objective."""
    try:
        records = await sessions_repo.get_by_objective(objective_id, limit, offset)
        return [ChatSessionResponse(**dict(record)) for record in records]

    except Exception as e:
        logger.error(f"Failed to list chat sessions: {e}")
        raise HTTPException(status_code=500, detail="Failed to list chat sessions")


@router.get("/chat/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: UUID,
    sessions_repo: ChatSessionsRepository = Depends(get_chat_sessions_repo),
) -> ChatSessionResponse:
    """Get a chat session by ID."""
    try:
        record = await sessions_repo.get_by_id(session_id)
        if not record:
            raise HTTPException(status_code=404, detail="Chat session not found")

        return ChatSessionResponse(**dict(record))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get chat session: {e}")
        raise HTTPException(status_code=500, detail="Failed to get chat session")


@router.delete("/chat/sessions/{session_id}", status_code=204)
async def delete_chat_session(
    session_id: UUID,
    sessions_repo: ChatSessionsRepository = Depends(get_chat_sessions_repo),
) -> None:
    """Delete a chat session."""
    try:
        deleted = await sessions_repo.delete(session_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Chat session not found")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete chat session: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete chat session")


@router.post("/chat/sessions/{session_id}/messages", response_model=MessageResponse)
async def send_message(
    session_id: UUID,
    message: MessageCreate,
    sessions_repo: ChatSessionsRepository = Depends(get_chat_sessions_repo),
    messages_repo: ChatMessagesRepository = Depends(get_chat_messages_repo),
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
) -> MessageResponse:
    """Send a message in a chat session and get agent response."""
    try:
        # Verify session exists
        session = await sessions_repo.get_by_id(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")

        # Save user message
        user_message_data = {
            "session_id": session_id,
            "role": "user",
            "content": message.content,
            "metadata": {},
            "sources": [],
        }
        await messages_repo.create(user_message_data)

        # Get conversation history
        history = await messages_repo.get_conversation_history(session_id, limit=10)

        # Create agent state
        agent_state: AgentState = {
            "query": message.content,
            "session_id": session_id,
            "objective_id": session["objective_id"],
            "conversation_history": history,
            "agent_path": [],
            "errors": [],
            "retry_count": 0,
        }

        # Execute agent orchestration
        result_state = await orchestrator.execute(agent_state)

        # Extract response
        response_text = result_state.get("response", "I encountered an error processing your request.")
        sources = result_state.get("sources", [])
        errors = result_state.get("errors", [])

        # Save agent message
        agent_message_data = {
            "session_id": session_id,
            "role": "agent",
            "agent_type": "conversation",
            "content": response_text,
            "metadata": {
                "agent_path": result_state.get("agent_path", []),
                "errors": errors,
            },
            "sources": sources,
        }
        agent_message_record = await messages_repo.create(agent_message_data)

        # Update session last message time
        await sessions_repo.update_last_message_time(session_id)

        # Convert database record to dict and process sources
        record_dict = dict(agent_message_record)
        db_sources = record_dict.pop('sources', [])
        source_citations = [SourceCitation(**src) for src in db_sources] if db_sources else []

        return MessageResponse(
            **record_dict,
            sources=source_citations,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to send message: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to send message")


@router.get("/chat/sessions/{session_id}/messages", response_model=list[MessageResponse])
async def get_messages(
    session_id: UUID,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    sessions_repo: ChatSessionsRepository = Depends(get_chat_sessions_repo),
    messages_repo: ChatMessagesRepository = Depends(get_chat_messages_repo),
) -> list[MessageResponse]:
    """Get message history for a session."""
    try:
        # Verify session exists
        session = await sessions_repo.get_by_id(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")

        records = await messages_repo.get_by_session(session_id, limit, offset)

        responses = []
        for record in records:
            record_dict = dict(record)
            db_sources = record_dict.pop('sources', [])
            source_citations = [SourceCitation(**src) for src in db_sources] if db_sources else []
            responses.append(MessageResponse(**record_dict, sources=source_citations))

        return responses

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get messages: {e}")
        raise HTTPException(status_code=500, detail="Failed to get messages")


@router.get("/chat/messages/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: UUID,
    messages_repo: ChatMessagesRepository = Depends(get_chat_messages_repo),
) -> MessageResponse:
    """Get a specific message by ID."""
    try:
        record = await messages_repo.get_by_id(message_id)
        if not record:
            raise HTTPException(status_code=404, detail="Message not found")

        sources = record.get("sources", [])
        source_citations = [SourceCitation(**src) for src in sources] if sources else []

        return MessageResponse(**dict(record), sources=source_citations)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get message: {e}")
        raise HTTPException(status_code=500, detail="Failed to get message")


@router.delete("/chat/messages/{message_id}", status_code=204)
async def delete_message(
    message_id: UUID,
    messages_repo: ChatMessagesRepository = Depends(get_chat_messages_repo),
) -> None:
    """Soft delete a message."""
    try:
        deleted = await messages_repo.soft_delete(message_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Message not found or already deleted")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete message")
