"""
Pydantic models for Apache AGE data structures.

These models provide runtime validation of AGE query results to catch
parsing issues early and ensure data integrity.
"""
import json
from typing import Any, Optional, Union
from pydantic import BaseModel, Field, field_validator, ValidationError


class AgeVertex(BaseModel):
    """
    Model for Apache AGE vertex (node) structure.

    AGE vertices have the format:
    {"id": <graphid>, "label": "LabelName", "properties": {...}}::vertex
    """

    id: int = Field(..., description="AGE internal graph ID")
    label: str = Field(..., description="Vertex label/type")
    properties: dict[str, Any] = Field(
        default_factory=dict, description="User-defined properties"
    )

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: int) -> int:
        """Validate that ID is a positive integer."""
        if v < 0:
            raise ValueError("AGE vertex ID must be non-negative")
        return v

    @field_validator("label")
    @classmethod
    def validate_label(cls, v: str) -> str:
        """Validate that label is non-empty."""
        if not v or not v.strip():
            raise ValueError("AGE vertex label cannot be empty")
        return v


class AgeEdge(BaseModel):
    """
    Model for Apache AGE edge (relationship) structure.

    AGE edges have the format:
    {"id": <graphid>, "label": "RELATIONSHIP_TYPE", "start_id": <id>, "end_id": <id>, "properties": {...}}::edge
    """

    id: int = Field(..., description="AGE internal graph ID")
    label: str = Field(..., description="Edge label/relationship type")
    start_id: int = Field(..., description="ID of source vertex")
    end_id: int = Field(..., description="ID of target vertex")
    properties: dict[str, Any] = Field(
        default_factory=dict, description="User-defined properties"
    )

    @field_validator("id", "start_id", "end_id")
    @classmethod
    def validate_ids(cls, v: int) -> int:
        """Validate that IDs are positive integers."""
        if v < 0:
            raise ValueError("AGE edge IDs must be non-negative")
        return v

    @field_validator("label")
    @classmethod
    def validate_label(cls, v: str) -> str:
        """Validate that label is non-empty."""
        if not v or not v.strip():
            raise ValueError("AGE edge label cannot be empty")
        return v


class EntityProperties(BaseModel):
    """
    Model for Entity node properties specific to KETA.

    This represents the expected structure within the 'properties'
    dict of an Entity vertex.
    """

    id: str = Field(..., description="Entity UUID")
    name: str = Field(..., description="Entity name")
    type: str = Field(..., description="Entity type (PERSON, ORGANIZATION, etc.)")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Extraction confidence score"
    )
    source_ids: list[str] = Field(
        default_factory=list, description="Source document UUIDs"
    )
    extraction_method: str = Field(
        default="llm_structured", description="Method used for extraction"
    )
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")

    @field_validator("type")
    @classmethod
    def validate_entity_type(cls, v: str) -> str:
        """Validate entity type is one of the expected values."""
        valid_types = {
            "PERSON",
            "ORGANIZATION",
            "LOCATION",
            "DATE",
            "PRODUCT",
            "CONCEPT",
            "EVENT",
        }
        if v.upper() not in valid_types:
            raise ValueError(
                f"Entity type must be one of {valid_types}, got: {v}"
            )
        return v.upper()


class RelationshipProperties(BaseModel):
    """
    Model for RELATED_TO edge properties specific to KETA.

    This represents the expected structure within the 'properties'
    dict of a RELATED_TO edge.
    """

    relationship_type: str = Field(..., description="Type of relationship")
    description: str = Field(..., description="Natural language description")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Extraction confidence score"
    )
    source_ids: list[str] = Field(
        default_factory=list, description="Source document UUIDs"
    )

    @field_validator("relationship_type")
    @classmethod
    def validate_relationship_type(cls, v: str) -> str:
        """Validate relationship type is non-empty."""
        if not v or not v.strip():
            raise ValueError("Relationship type cannot be empty")
        return v


class RelationshipResult(BaseModel):
    """
    Model for relationship query results.

    This represents the structure returned by queries like:
    RETURN {source_entity: e1, relationship: r, target_entity: e2}
    """

    source_entity: AgeVertex = Field(..., description="Source entity vertex")
    relationship: AgeEdge = Field(..., description="Relationship edge")
    target_entity: AgeVertex = Field(..., description="Target entity vertex")

    def get_source_properties(self) -> EntityProperties:
        """Extract and validate source entity properties."""
        return EntityProperties(**self.source_entity.properties)

    def get_target_properties(self) -> EntityProperties:
        """Extract and validate target entity properties."""
        return EntityProperties(**self.target_entity.properties)

    def get_relationship_properties(self) -> RelationshipProperties:
        """Extract and validate relationship properties."""
        return RelationshipProperties(**self.relationship.properties)


class GraphStatistics(BaseModel):
    """Model for graph statistics query results."""

    entity_count: int = Field(default=0, description="Total number of entities")
    relationship_count: int = Field(
        default=0, description="Total number of relationships"
    )
    entity_type_counts: dict[str, int] = Field(
        default_factory=dict, description="Count of entities by type"
    )
    relationship_type_counts: dict[str, int] = Field(
        default_factory=dict, description="Count of relationships by type"
    )

    @field_validator("entity_count", "relationship_count")
    @classmethod
    def validate_counts(cls, v: int) -> int:
        """Validate counts are non-negative."""
        if v < 0:
            raise ValueError("Counts must be non-negative")
        return v


# Alias for consistency with AGE naming conventions
AgeRelationshipResult = RelationshipResult


class AgeParseError(Exception):
    """Custom exception for AGE data parsing errors."""
    
    def __init__(self, message: str, raw_data: Optional[str] = None, context: Optional[dict] = None):
        self.message = message
        self.raw_data = raw_data
        self.context = context or {}
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        """Format error message with context."""
        msg = f"AGE Parsing Error: {self.message}"
        if self.context:
            msg += f"\nContext: {self.context}"
        if self.raw_data:
            sample = self.raw_data[:200] if len(self.raw_data) > 200 else self.raw_data
            msg += f"\nRaw data sample: {sample}"
        return msg


def parse_agtype_to_vertex(agtype_data: Union[str, dict]) -> AgeVertex:
    """
    Parse AGE agtype data to AgeVertex with validation.
    
    Args:
        agtype_data: Raw AGE vertex data (string or dict)
        
    Returns:
        Validated AgeVertex instance
        
    Raises:
        AgeParseError: If parsing or validation fails
    """
    try:
        # Handle string format: {...}::vertex
        if isinstance(agtype_data, str):
            json_str = agtype_data.replace('::vertex', '').strip()
            parsed = json.loads(json_str)
        elif isinstance(agtype_data, dict):
            parsed = agtype_data
        else:
            raise AgeParseError(
                f"Expected string or dict, got {type(agtype_data)}",
                raw_data=str(agtype_data),
                context={"input_type": type(agtype_data).__name__}
            )
        
        # Validate structure
        return AgeVertex(**parsed)
        
    except json.JSONDecodeError as e:
        raise AgeParseError(
            "Invalid JSON in agtype vertex data",
            raw_data=str(agtype_data),
            context={"json_error": str(e)}
        ) from e
    except ValidationError as e:
        raise AgeParseError(
            "Vertex data failed validation",
            raw_data=str(agtype_data),
            context={"validation_errors": e.errors()}
        ) from e
    except Exception as e:
        raise AgeParseError(
            f"Unexpected error parsing vertex: {type(e).__name__}",
            raw_data=str(agtype_data),
            context={"error": str(e)}
        ) from e


def parse_agtype_to_edge(agtype_data: Union[str, dict]) -> AgeEdge:
    """
    Parse AGE agtype data to AgeEdge with validation.
    
    Args:
        agtype_data: Raw AGE edge data (string or dict)
        
    Returns:
        Validated AgeEdge instance
        
    Raises:
        AgeParseError: If parsing or validation fails
    """
    try:
        # Handle string format: {...}::edge
        if isinstance(agtype_data, str):
            json_str = agtype_data.replace('::edge', '').strip()
            parsed = json.loads(json_str)
        elif isinstance(agtype_data, dict):
            parsed = agtype_data
        else:
            raise AgeParseError(
                f"Expected string or dict, got {type(agtype_data)}",
                raw_data=str(agtype_data),
                context={"input_type": type(agtype_data).__name__}
            )
        
        # Validate structure
        return AgeEdge(**parsed)
        
    except json.JSONDecodeError as e:
        raise AgeParseError(
            "Invalid JSON in agtype edge data",
            raw_data=str(agtype_data),
            context={"json_error": str(e)}
        ) from e
    except ValidationError as e:
        raise AgeParseError(
            "Edge data failed validation",
            raw_data=str(agtype_data),
            context={"validation_errors": e.errors()}
        ) from e
    except Exception as e:
        raise AgeParseError(
            f"Unexpected error parsing edge: {type(e).__name__}",
            raw_data=str(agtype_data),
            context={"error": str(e)}
        ) from e


def validate_entity_properties(properties: dict[str, Any]) -> EntityProperties:
    """
    Validate entity properties with clear error messages.
    
    Args:
        properties: Dictionary of entity properties
        
    Returns:
        Validated EntityProperties instance
        
    Raises:
        AgeParseError: If validation fails
    """
    try:
        return EntityProperties(**properties)
    except ValidationError as e:
        raise AgeParseError(
            "Entity properties failed validation",
            raw_data=json.dumps(properties, default=str),
            context={
                "validation_errors": e.errors(),
                "missing_fields": [err["loc"][0] for err in e.errors() if err["type"] == "missing"],
            }
        ) from e


def validate_relationship_properties(properties: dict[str, Any]) -> RelationshipProperties:
    """
    Validate relationship properties with clear error messages.
    
    Args:
        properties: Dictionary of relationship properties
        
    Returns:
        Validated RelationshipProperties instance
        
    Raises:
        AgeParseError: If validation fails
    """
    try:
        return RelationshipProperties(**properties)
    except ValidationError as e:
        raise AgeParseError(
            "Relationship properties failed validation",
            raw_data=json.dumps(properties, default=str),
            context={
                "validation_errors": e.errors(),
                "missing_fields": [err["loc"][0] for err in e.errors() if err["type"] == "missing"],
            }
        ) from e
