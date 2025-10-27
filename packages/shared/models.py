"""
Shared Pydantic models for KETA API.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ============================================
# ENUMS
# ============================================


class ObjectiveStatus(str, Enum):
    """Objective status enumeration."""

    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


class ExtractionStatus(str, Enum):
    """Source extraction status enumeration."""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ChatSessionStatus(str, Enum):
    """Chat session status enumeration."""

    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class MessageRole(str, Enum):
    """Message role enumeration."""

    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"


class AgentType(str, Enum):
    """Agent type enumeration."""

    EXTRACTION = "extraction"
    CONVERSATION = "conversation"


class EntityType(str, Enum):
    """Entity type enumeration."""

    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    DATE = "DATE"
    PRODUCT = "PRODUCT"
    CONCEPT = "CONCEPT"
    EVENT = "EVENT"


# ============================================
# BASE MODELS
# ============================================


class BaseResponse(BaseModel):
    """Base response model."""

    id: UUID
    created_at: datetime


# ============================================
# OBJECTIVE MODELS
# ============================================


class ObjectiveCreate(BaseModel):
    """Request model for creating an objective."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    domain: Optional[str] = Field(None, max_length=100)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ObjectiveUpdate(BaseModel):
    """Request model for updating an objective."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    domain: Optional[str] = Field(None, max_length=100)
    status: Optional[ObjectiveStatus] = None
    metadata: Optional[dict[str, Any]] = None


class ObjectiveResponse(BaseResponse):
    """Response model for an objective."""

    name: str
    description: Optional[str]
    domain: Optional[str]
    status: ObjectiveStatus
    updated_at: datetime
    metadata: dict[str, Any]


class ObjectiveStats(BaseModel):
    """Statistics for an objective."""

    id: UUID
    name: str
    status: ObjectiveStatus
    source_count: int
    completed_sources: int
    failed_sources: int
    session_count: int
    message_count: int
    last_processed_at: Optional[datetime]
    last_chat_at: Optional[datetime]


# ============================================
# SOURCE MODELS
# ============================================


class SourceCreate(BaseModel):
    """Request model for creating a source."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    content: str = Field(..., min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SourceResponse(BaseModel):
    """Response model for a source."""

    id: UUID
    objective_id: UUID
    name: str
    description: Optional[str]
    content_type: str
    content: str
    extraction_status: ExtractionStatus
    extraction_progress: dict[str, Any]
    extraction_error: Optional[str]
    uploaded_at: datetime
    processed_at: Optional[datetime]
    metadata: dict[str, Any]


class ExtractionProgress(BaseModel):
    """Extraction progress information."""

    total_chunks: int = 0
    processed_chunks: int = 0
    entities_extracted: int = 0
    relationships_extracted: int = 0
    current_stage: Optional[str] = None


class ExtractionStatusResponse(BaseModel):
    """Response for extraction status check."""

    source_id: UUID
    status: ExtractionStatus
    progress: ExtractionProgress
    error: Optional[str] = None


# ============================================
# CHAT SESSION MODELS
# ============================================


class ChatSessionCreate(BaseModel):
    """Request model for creating a chat session."""

    objective_id: UUID
    name: Optional[str] = Field(None, max_length=255)
    scope_source_ids: list[UUID] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatSessionResponse(BaseResponse):
    """Response model for a chat session."""

    objective_id: UUID
    name: Optional[str]
    status: ChatSessionStatus
    scope_source_ids: list[UUID]
    last_message_at: Optional[datetime]
    metadata: dict[str, Any]


# ============================================
# CHAT MESSAGE MODELS
# ============================================


class SourceCitation(BaseModel):
    """Source citation for a message."""

    source_id: UUID
    source_name: str
    snippet: str
    relevance_score: Optional[float] = None


class MessageCreate(BaseModel):
    """Request model for sending a message."""

    content: str = Field(..., min_length=1)


class MessageResponse(BaseResponse):
    """Response model for a chat message."""

    session_id: UUID
    role: MessageRole
    agent_type: Optional[AgentType]
    content: str
    metadata: dict[str, Any]
    sources: list[SourceCitation]
    deleted_at: Optional[datetime] = None


# ============================================
# GRAPH MODELS
# ============================================


class EntityResponse(BaseModel):
    """Response model for an entity."""

    id: UUID
    name: str
    type: EntityType
    source_ids: list[UUID]
    confidence: float = Field(..., ge=0.0, le=1.0)
    extraction_method: str
    created_at: datetime
    updated_at: datetime


class RelationshipResponse(BaseModel):
    """Response model for a relationship."""

    entity1_id: UUID
    entity1_name: str
    entity2_id: UUID
    entity2_name: str
    relationship_type: str
    description: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    source_ids: list[UUID]


class GraphVisualizationNode(BaseModel):
    """Node for graph visualization."""

    id: str
    label: str
    type: str
    properties: dict[str, Any]


class GraphVisualizationEdge(BaseModel):
    """Edge for graph visualization."""

    source: str
    target: str
    label: str
    properties: dict[str, Any]


class GraphVisualizationData(BaseModel):
    """Complete graph visualization data."""

    nodes: list[GraphVisualizationNode]
    edges: list[GraphVisualizationEdge]


class GraphStats(BaseModel):
    """Graph statistics for an objective."""

    objective_id: UUID
    total_entities: int
    total_relationships: int
    entity_type_counts: dict[str, int]
    relationship_type_counts: dict[str, int]


# ============================================
# HEALTH CHECK MODELS
# ============================================


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    database: bool
    graph: bool
    timestamp: datetime


# ============================================
# ERROR MODELS
# ============================================


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
