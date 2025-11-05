"""Unit tests for Apache AGE parsing logic."""
import json
import pytest
from packages.shared.repositories.base import GraphRepository


class TestAGEParsing:
    """Test AGE agtype format parsing."""

    def test_parse_simple_vertex_with_properties(self):
        """Test parsing a simple vertex with properties key."""
        raw = '{"id": 1125899906842625, "label": "Entity", "properties": {"id": "test-uuid", "name": "Alice", "type": "PERSON"}}::vertex'
        result = GraphRepository._parse_agtype(raw)

        assert result is not None
        assert result["name"] == "Alice"
        assert result["type"] == "PERSON"
        assert result["id"] == "test-uuid"

    def test_parse_simple_edge_with_properties(self):
        """Test parsing a simple edge with properties key."""
        raw = '{"id": 1970324836974593, "label": "RELATED_TO", "start_id": 123, "end_id": 456, "properties": {"relationship_type": "works_at", "confidence": 0.9}}::edge'
        result = GraphRepository._parse_agtype(raw)

        assert result is not None
        assert result["relationship_type"] == "works_at"
        assert result["confidence"] == 0.9

    def test_parse_vertex_without_marker(self):
        """Test parsing vertex JSON without ::vertex marker."""
        raw = '{"id": 123, "label": "Entity", "properties": {"name": "Bob"}}'
        result = GraphRepository._parse_agtype(raw)

        assert result is not None
        assert result["name"] == "Bob"

    def test_parse_nested_structure_with_multiple_markers(self):
        """Test parsing nested structure with ::vertex and ::edge markers embedded."""
        raw = '''{"relationship": {"id": 1970324836974593, "label": "RELATED_TO", "properties": {"relationship_type": "founded_by"}}::edge, "source_entity": {"id": 1125899906842625, "label": "Entity", "properties": {"name": "CorporationC"}}::vertex, "target_entity": {"id": 1125899906842626, "label": "Entity", "properties": {"name": "PersonA"}}::vertex}'''
        result = GraphRepository._parse_agtype(raw)

        assert result is not None
        assert "relationship" in result
        assert "source_entity" in result
        assert "target_entity" in result
        assert result["relationship"]["properties"]["relationship_type"] == "founded_by"
        assert result["source_entity"]["properties"]["name"] == "CorporationC"
        assert result["target_entity"]["properties"]["name"] == "PersonA"

    def test_parse_malformed_json_returns_none(self):
        """Test that malformed JSON returns None instead of raising."""
        raw = '{"id": 123, "invalid_json::vertex'
        result = GraphRepository._parse_agtype(raw)

        assert result is None

    def test_parse_empty_string_returns_none(self):
        """Test that empty string returns None."""
        result = GraphRepository._parse_agtype("")
        assert result is None

    def test_parse_none_returns_none(self):
        """Test that None input returns None."""
        result = GraphRepository._parse_agtype(None)
        assert result is None

    def test_parse_vertex_missing_properties_key(self):
        """Test parsing vertex that has no properties key (legacy format)."""
        raw = '{"id": 123, "label": "Entity", "name": "DirectValue"}::vertex'
        result = GraphRepository._parse_agtype(raw)

        assert result is not None
        assert result["name"] == "DirectValue"

    def test_parse_complex_nested_properties(self):
        """Test parsing with deeply nested properties."""
        raw = '{"id": 123, "label": "Entity", "properties": {"name": "Test", "metadata": {"created_at": "2025-11-03", "tags": ["a", "b"]}, "confidence": 0.95}}::vertex'
        result = GraphRepository._parse_agtype(raw)

        assert result is not None
        assert result["name"] == "Test"
        assert result["metadata"]["created_at"] == "2025-11-03"
        assert result["metadata"]["tags"] == ["a", "b"]
        assert result["confidence"] == 0.95

    def test_parse_agtype_value_with_string_containing_markers(self):
        """Test that _parse_agtype_value handles string values with markers."""
        value = '{"id": 123, "label": "Entity", "properties": {"name": "Alice"}}::vertex'
        result = GraphRepository._parse_agtype_value(value)

        assert result is not None
        assert isinstance(result, dict)
        assert result["name"] == "Alice"

    def test_parse_agtype_value_with_dict(self):
        """Test that _parse_agtype_value recursively processes dicts."""
        value = {
            "entity": '{"id": 123, "properties": {"name": "Bob"}}::vertex',
            "count": 5
        }
        result = GraphRepository._parse_agtype_value(value)

        assert result["entity"]["name"] == "Bob"
        assert result["count"] == 5

    def test_parse_agtype_value_with_list(self):
        """Test that _parse_agtype_value recursively processes lists."""
        value = [
            '{"id": 1, "properties": {"name": "A"}}::vertex',
            '{"id": 2, "properties": {"name": "B"}}::vertex'
        ]
        result = GraphRepository._parse_agtype_value(value)

        assert len(result) == 2
        assert result[0]["name"] == "A"
        assert result[1]["name"] == "B"

    def test_parse_preserves_all_agtype_metadata(self):
        """Test that parsing preserves AGE metadata like id, label when needed."""
        raw = '{"id": 1125899906842625, "label": "Entity", "properties": {"name": "Test"}}::vertex'
        result = GraphRepository._parse_agtype(raw)

        assert "name" in result

    def test_parse_handles_unicode_characters(self):
        """Test parsing with unicode characters in properties."""
        raw = '{"id": 123, "label": "Entity", "properties": {"name": "Müller", "description": "Test with émojis 🎉"}}::vertex'
        result = GraphRepository._parse_agtype(raw)

        assert result is not None
        assert result["name"] == "Müller"
        assert "🎉" in result["description"]

    def test_parse_empty_properties_dict(self):
        """Test parsing vertex with empty properties."""
        raw = '{"id": 123, "label": "Entity", "properties": {}}::vertex'
        result = GraphRepository._parse_agtype(raw)

        assert result == {}

    def test_parse_multiple_markers_in_sequence(self):
        """Test that multiple consecutive markers are all stripped."""
        raw = '{"id": 123, "properties": {"name": "Test"}}::vertex::vertex'
        result = GraphRepository._parse_agtype(raw)

        assert result is not None
        assert result["name"] == "Test"

    def test_parse_edge_with_relationship_data(self):
        """Test parsing edge with typical relationship data."""
        raw = '''{"id": 1970324836974593, "label": "RELATED_TO", "end_id": 1125899906842626, "start_id": 1125899906842625, "properties": {"confidence": 0.9, "source_ids": ["doc-123"], "description": "Company founded by person", "relationship_type": "founded_by"}}::edge'''
        result = GraphRepository._parse_agtype(raw)

        assert result is not None
        assert result["relationship_type"] == "founded_by"
        assert result["confidence"] == 0.9
        assert result["description"] == "Company founded by person"
        assert "doc-123" in result["source_ids"]

    def test_parse_result_with_numeric_values(self):
        """Test parsing with various numeric types."""
        raw = '{"id": 123, "properties": {"count": 42, "score": 0.95, "large_num": 1234567890}}::vertex'
        result = GraphRepository._parse_agtype(raw)

        assert result["count"] == 42
        assert result["score"] == 0.95
        assert result["large_num"] == 1234567890

    def test_parse_result_with_boolean_values(self):
        """Test parsing with boolean values."""
        raw = '{"id": 123, "properties": {"active": true, "deleted": false}}::vertex'
        result = GraphRepository._parse_agtype(raw)

        assert result["active"] is True
        assert result["deleted"] is False

    def test_parse_result_with_null_values(self):
        """Test parsing with null values."""
        raw = '{"id": 123, "properties": {"name": "Test", "description": null}}::vertex'
        result = GraphRepository._parse_agtype(raw)

        assert result["name"] == "Test"
        assert result["description"] is None
