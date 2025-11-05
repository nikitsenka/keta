"""
Shared models package.
"""

# Import core models from core.py
from packages.shared.models.core import (
    ObjectiveStatus,
    ExtractionStatus,
    ChatSessionStatus,
    MessageRole,
    AgentType,
    EntityType,
    BaseResponse,
    ObjectiveCreate,
    ObjectiveUpdate,
    ObjectiveResponse,
    ObjectiveStats,
    SourceCreate,
    SourceResponse,
    ExtractionProgress,
    ExtractionStatusResponse,
    ChatSessionCreate,
    ChatSessionResponse,
    SourceCitation,
    MessageCreate,
    MessageResponse,
    EntityResponse,
    RelationshipResponse,
    GraphVisualizationNode,
    GraphVisualizationEdge,
    GraphVisualizationData,
    GraphStats,
    HealthCheckResponse,
    ErrorResponse,
)

# Import AGE models
from packages.shared.models.age import (
    AgeVertex,
    AgeEdge,
    AgeRelationshipResult,
    EntityProperties,
    RelationshipProperties,
    RelationshipResult,
    GraphStatistics,
    AgeParseError,
    parse_agtype_to_vertex,
    parse_agtype_to_edge,
    validate_entity_properties,
    validate_relationship_properties,
)

__all__ = [
    # Enums
    "ObjectiveStatus",
    "ExtractionStatus",
    "ChatSessionStatus",
    "MessageRole",
    "AgentType",
    "EntityType",
    # Base models
    "BaseResponse",
    # Objective models
    "ObjectiveCreate",
    "ObjectiveUpdate",
    "ObjectiveResponse",
    "ObjectiveStats",
    # Source models
    "SourceCreate",
    "SourceResponse",
    "ExtractionProgress",
    "ExtractionStatusResponse",
    # Chat models
    "ChatSessionCreate",
    "ChatSessionResponse",
    "SourceCitation",
    "MessageCreate",
    "MessageResponse",
    # Graph models
    "EntityResponse",
    "RelationshipResponse",
    "GraphVisualizationNode",
    "GraphVisualizationEdge",
    "GraphVisualizationData",
    "GraphStats",
    # Health/Error models
    "HealthCheckResponse",
    "ErrorResponse",
    # AGE models
    "AgeVertex",
    "AgeEdge",
    "AgeRelationshipResult",
    "EntityProperties",
    "RelationshipProperties",
    "RelationshipResult",
    "GraphStatistics",
    "AgeParseError",
    "parse_agtype_to_vertex",
    "parse_agtype_to_edge",
    "validate_entity_properties",
    "validate_relationship_properties",
]
