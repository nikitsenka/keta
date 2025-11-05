"""Unit tests for Apache AGE Pydantic models."""
import json
import pytest
from pydantic import ValidationError

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


class TestAgeVertex:
    """Test AgeVertex model validation."""

    def test_valid_vertex(self):
        """Test creating a valid vertex."""
        vertex = AgeVertex(
            id=1125899906842625,
            label="Entity",
            properties={"name": "Alice", "type": "PERSON"},
        )
        assert vertex.id == 1125899906842625
        assert vertex.label == "Entity"
        assert vertex.properties["name"] == "Alice"

    def test_vertex_with_empty_properties(self):
        """Test vertex with no properties."""
        vertex = AgeVertex(id=123, label="Node")
        assert vertex.properties == {}

    def test_vertex_negative_id_fails(self):
        """Test that negative ID fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            AgeVertex(id=-1, label="Entity", properties={})
        
        errors = exc_info.value.errors()
        assert any("non-negative" in str(e["msg"]).lower() for e in errors)

    def test_vertex_empty_label_fails(self):
        """Test that empty label fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            AgeVertex(id=123, label="", properties={})
        
        errors = exc_info.value.errors()
        assert any("empty" in str(e["msg"]).lower() for e in errors)

    def test_vertex_whitespace_label_fails(self):
        """Test that whitespace-only label fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            AgeVertex(id=123, label="   ", properties={})
        
        errors = exc_info.value.errors()
        assert any("empty" in str(e["msg"]).lower() for e in errors)

    def test_vertex_missing_required_fields(self):
        """Test that missing required fields fail validation."""
        with pytest.raises(ValidationError) as exc_info:
            AgeVertex(label="Entity")
        
        errors = exc_info.value.errors()
        assert any(e["loc"][0] == "id" for e in errors)


class TestAgeEdge:
    """Test AgeEdge model validation."""

    def test_valid_edge(self):
        """Test creating a valid edge."""
        edge = AgeEdge(
            id=1970324836974593,
            label="RELATED_TO",
            start_id=123,
            end_id=456,
            properties={"relationship_type": "works_at"},
        )
        assert edge.id == 1970324836974593
        assert edge.label == "RELATED_TO"
        assert edge.start_id == 123
        assert edge.end_id == 456

    def test_edge_with_empty_properties(self):
        """Test edge with no properties."""
        edge = AgeEdge(id=1, label="KNOWS", start_id=10, end_id=20)
        assert edge.properties == {}

    def test_edge_negative_ids_fail(self):
        """Test that negative IDs fail validation."""
        with pytest.raises(ValidationError):
            AgeEdge(id=-1, label="REL", start_id=10, end_id=20)
        
        with pytest.raises(ValidationError):
            AgeEdge(id=1, label="REL", start_id=-10, end_id=20)
        
        with pytest.raises(ValidationError):
            AgeEdge(id=1, label="REL", start_id=10, end_id=-20)

    def test_edge_empty_label_fails(self):
        """Test that empty label fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            AgeEdge(id=1, label="", start_id=10, end_id=20)
        
        errors = exc_info.value.errors()
        assert any("empty" in str(e["msg"]).lower() for e in errors)


class TestEntityProperties:
    """Test EntityProperties model validation."""

    def test_valid_entity_properties(self):
        """Test creating valid entity properties."""
        props = EntityProperties(
            id="uuid-123",
            name="Alice",
            type="PERSON",
            confidence=0.95,
            source_ids=["source-1", "source-2"],
            extraction_method="llm_structured",
        )
        assert props.id == "uuid-123"
        assert props.name == "Alice"
        assert props.type == "PERSON"
        assert props.confidence == 0.95

    def test_entity_type_normalization(self):
        """Test that entity type is normalized to uppercase."""
        props = EntityProperties(
            id="uuid-123", name="Bob", type="person", confidence=0.8
        )
        assert props.type == "PERSON"

    def test_invalid_entity_type_fails(self):
        """Test that invalid entity type fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            EntityProperties(
                id="uuid-123", name="Bob", type="INVALID_TYPE", confidence=0.8
            )
        
        errors = exc_info.value.errors()
        assert any("entity type" in str(e["msg"]).lower() for e in errors)

    def test_confidence_out_of_range_fails(self):
        """Test that confidence outside [0, 1] fails validation."""
        with pytest.raises(ValidationError):
            EntityProperties(
                id="uuid-123", name="Bob", type="PERSON", confidence=1.5
            )
        
        with pytest.raises(ValidationError):
            EntityProperties(
                id="uuid-123", name="Bob", type="PERSON", confidence=-0.1
            )

    def test_entity_properties_with_defaults(self):
        """Test entity properties with default values."""
        props = EntityProperties(
            id="uuid-123", name="Alice", type="PERSON", confidence=0.9
        )
        assert props.source_ids == []
        assert props.extraction_method == "llm_structured"
        assert props.created_at is None
        assert props.updated_at is None


class TestRelationshipProperties:
    """Test RelationshipProperties model validation."""

    def test_valid_relationship_properties(self):
        """Test creating valid relationship properties."""
        props = RelationshipProperties(
            relationship_type="works_at",
            description="Alice works at Company X",
            confidence=0.9,
            source_ids=["source-1"],
        )
        assert props.relationship_type == "works_at"
        assert props.description == "Alice works at Company X"
        assert props.confidence == 0.9

    def test_relationship_empty_type_fails(self):
        """Test that empty relationship type fails validation."""
        with pytest.raises(ValidationError):
            RelationshipProperties(
                relationship_type="",
                description="Test",
                confidence=0.8,
            )

    def test_relationship_confidence_validation(self):
        """Test relationship confidence validation."""
        with pytest.raises(ValidationError):
            RelationshipProperties(
                relationship_type="works_at",
                description="Test",
                confidence=2.0,
            )


class TestRelationshipResult:
    """Test RelationshipResult model validation."""

    def test_valid_relationship_result(self):
        """Test creating a valid relationship result."""
        source = AgeVertex(
            id=1, label="Entity", properties={"id": "e1", "name": "Alice", "type": "PERSON", "confidence": 0.9}
        )
        edge = AgeEdge(
            id=2,
            label="RELATED_TO",
            start_id=1,
            end_id=3,
            properties={
                "relationship_type": "works_at",
                "description": "Alice works at Company X",
                "confidence": 0.85,
                "source_ids": ["source-1"],
            },
        )
        target = AgeVertex(
            id=3, label="Entity", properties={"id": "e2", "name": "Company X", "type": "ORGANIZATION", "confidence": 0.95}
        )

        result = RelationshipResult(
            source_entity=source, relationship=edge, target_entity=target
        )
        
        assert result.source_entity.id == 1
        assert result.relationship.id == 2
        assert result.target_entity.id == 3

    def test_relationship_result_property_extraction(self):
        """Test extracting validated properties from relationship result."""
        source = AgeVertex(
            id=1,
            label="Entity",
            properties={
                "id": "e1",
                "name": "Alice",
                "type": "PERSON",
                "confidence": 0.9,
            },
        )
        edge = AgeEdge(
            id=2,
            label="RELATED_TO",
            start_id=1,
            end_id=3,
            properties={
                "relationship_type": "works_at",
                "description": "Test relationship",
                "confidence": 0.85,
                "source_ids": [],
            },
        )
        target = AgeVertex(
            id=3,
            label="Entity",
            properties={
                "id": "e2",
                "name": "Company X",
                "type": "ORGANIZATION",
                "confidence": 0.95,
            },
        )

        result = RelationshipResult(
            source_entity=source, relationship=edge, target_entity=target
        )

        # Extract and validate properties
        source_props = result.get_source_properties()
        assert isinstance(source_props, EntityProperties)
        assert source_props.name == "Alice"

        target_props = result.get_target_properties()
        assert isinstance(target_props, EntityProperties)
        assert target_props.name == "Company X"

        rel_props = result.get_relationship_properties()
        assert isinstance(rel_props, RelationshipProperties)
        assert rel_props.relationship_type == "works_at"

    def test_age_relationship_result_alias(self):
        """Test that AgeRelationshipResult is an alias for RelationshipResult."""
        assert AgeRelationshipResult is RelationshipResult


class TestGraphStatistics:
    """Test GraphStatistics model validation."""

    def test_valid_graph_statistics(self):
        """Test creating valid graph statistics."""
        stats = GraphStatistics(
            entity_count=100,
            relationship_count=50,
            entity_type_counts={"PERSON": 60, "ORGANIZATION": 40},
            relationship_type_counts={"works_at": 30, "knows": 20},
        )
        assert stats.entity_count == 100
        assert stats.relationship_count == 50

    def test_graph_statistics_with_defaults(self):
        """Test graph statistics with default values."""
        stats = GraphStatistics()
        assert stats.entity_count == 0
        assert stats.relationship_count == 0
        assert stats.entity_type_counts == {}
        assert stats.relationship_type_counts == {}

    def test_negative_counts_fail(self):
        """Test that negative counts fail validation."""
        with pytest.raises(ValidationError):
            GraphStatistics(entity_count=-1)
        
        with pytest.raises(ValidationError):
            GraphStatistics(relationship_count=-5)


class TestParseAgtypeToVertex:
    """Test parse_agtype_to_vertex function."""

    def test_parse_vertex_from_string(self):
        """Test parsing vertex from AGE string format."""
        raw = '{"id": 1125899906842625, "label": "Entity", "properties": {"name": "Alice"}}::vertex'
        vertex = parse_agtype_to_vertex(raw)
        
        assert isinstance(vertex, AgeVertex)
        assert vertex.id == 1125899906842625
        assert vertex.label == "Entity"
        assert vertex.properties["name"] == "Alice"

    def test_parse_vertex_from_dict(self):
        """Test parsing vertex from dict."""
        data = {
            "id": 123,
            "label": "Node",
            "properties": {"key": "value"}
        }
        vertex = parse_agtype_to_vertex(data)
        
        assert isinstance(vertex, AgeVertex)
        assert vertex.id == 123
        assert vertex.label == "Node"

    def test_parse_vertex_invalid_json_raises_error(self):
        """Test that invalid JSON raises AgeParseError."""
        raw = '{"id": invalid}::vertex'
        
        with pytest.raises(AgeParseError) as exc_info:
            parse_agtype_to_vertex(raw)
        
        assert "Invalid JSON" in str(exc_info.value)
        assert exc_info.value.raw_data is not None

    def test_parse_vertex_invalid_structure_raises_error(self):
        """Test that invalid structure raises AgeParseError with validation details."""
        raw = '{"id": -1, "label": ""}::vertex'
        
        with pytest.raises(AgeParseError) as exc_info:
            parse_agtype_to_vertex(raw)
        
        assert "failed validation" in str(exc_info.value)
        assert "validation_errors" in exc_info.value.context

    def test_parse_vertex_wrong_type_raises_error(self):
        """Test that wrong input type raises AgeParseError."""
        with pytest.raises(AgeParseError) as exc_info:
            parse_agtype_to_vertex(12345)
        
        assert "Expected string or dict" in str(exc_info.value)


class TestParseAgtypeToEdge:
    """Test parse_agtype_to_edge function."""

    def test_parse_edge_from_string(self):
        """Test parsing edge from AGE string format."""
        raw = '{"id": 1970324836974593, "label": "KNOWS", "start_id": 1, "end_id": 2, "properties": {}}::edge'
        edge = parse_agtype_to_edge(raw)
        
        assert isinstance(edge, AgeEdge)
        assert edge.id == 1970324836974593
        assert edge.label == "KNOWS"
        assert edge.start_id == 1
        assert edge.end_id == 2

    def test_parse_edge_from_dict(self):
        """Test parsing edge from dict."""
        data = {
            "id": 100,
            "label": "REL",
            "start_id": 10,
            "end_id": 20,
            "properties": {"weight": 0.5}
        }
        edge = parse_agtype_to_edge(data)
        
        assert isinstance(edge, AgeEdge)
        assert edge.properties["weight"] == 0.5

    def test_parse_edge_invalid_json_raises_error(self):
        """Test that invalid JSON raises AgeParseError."""
        raw = '{"invalid json::edge'
        
        with pytest.raises(AgeParseError) as exc_info:
            parse_agtype_to_edge(raw)
        
        assert "Invalid JSON" in str(exc_info.value)

    def test_parse_edge_missing_fields_raises_error(self):
        """Test that missing required fields raises AgeParseError."""
        raw = '{"id": 1, "label": "REL"}::edge'
        
        with pytest.raises(AgeParseError) as exc_info:
            parse_agtype_to_edge(raw)
        
        assert "failed validation" in str(exc_info.value)


class TestValidateEntityProperties:
    """Test validate_entity_properties function."""

    def test_validate_valid_properties(self):
        """Test validating valid entity properties."""
        props = {
            "id": "uuid-123",
            "name": "Alice",
            "type": "PERSON",
            "confidence": 0.9,
        }
        result = validate_entity_properties(props)
        
        assert isinstance(result, EntityProperties)
        assert result.name == "Alice"

    def test_validate_invalid_properties_raises_error(self):
        """Test that invalid properties raise AgeParseError with context."""
        props = {
            "name": "Alice",
            "type": "PERSON",
            # Missing required 'id' and 'confidence'
        }
        
        with pytest.raises(AgeParseError) as exc_info:
            validate_entity_properties(props)
        
        error = exc_info.value
        assert "failed validation" in str(error)
        assert "missing_fields" in error.context
        assert "id" in error.context["missing_fields"] or "confidence" in error.context["missing_fields"]

    def test_validate_properties_with_invalid_type(self):
        """Test validating properties with invalid entity type."""
        props = {
            "id": "uuid-123",
            "name": "Alice",
            "type": "INVALID",
            "confidence": 0.9,
        }
        
        with pytest.raises(AgeParseError) as exc_info:
            validate_entity_properties(props)
        
        assert "validation" in str(exc_info.value).lower()


class TestValidateRelationshipProperties:
    """Test validate_relationship_properties function."""

    def test_validate_valid_relationship(self):
        """Test validating valid relationship properties."""
        props = {
            "relationship_type": "works_at",
            "description": "Test relationship",
            "confidence": 0.85,
        }
        result = validate_relationship_properties(props)
        
        assert isinstance(result, RelationshipProperties)
        assert result.relationship_type == "works_at"

    def test_validate_invalid_relationship_raises_error(self):
        """Test that invalid relationship properties raise AgeParseError."""
        props = {
            "description": "Test relationship",
            # Missing required 'relationship_type' and 'confidence'
        }
        
        with pytest.raises(AgeParseError) as exc_info:
            validate_relationship_properties(props)
        
        error = exc_info.value
        assert "failed validation" in str(error)
        assert "missing_fields" in error.context


class TestAgeParseError:
    """Test AgeParseError exception."""

    def test_error_message_formatting(self):
        """Test that error message is properly formatted."""
        error = AgeParseError(
            "Test error",
            raw_data='{"some": "data"}',
            context={"key": "value"}
        )
        
        message = str(error)
        assert "AGE Parsing Error: Test error" in message
        assert "Context: " in message
        assert "Raw data sample: " in message

    def test_error_with_long_raw_data(self):
        """Test that long raw data is truncated in error message."""
        long_data = "x" * 300
        error = AgeParseError("Test error", raw_data=long_data)
        
        message = str(error)
        assert len(message) < len(long_data) + 100  # Should be truncated

    def test_error_without_context(self):
        """Test error message without context."""
        error = AgeParseError("Test error")
        
        message = str(error)
        assert "AGE Parsing Error: Test error" in message
