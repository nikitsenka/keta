"""
Extraction tools for KETA agents.
"""

import json
import logging
from typing import Any
from uuid import UUID, uuid4

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ============================================
# STRUCTURED OUTPUT MODELS
# ============================================


class ExtractedEntity(BaseModel):
    """Model for a single extracted entity."""

    name: str = Field(description="Entity name")
    type: str = Field(description="Entity type (PERSON, ORGANIZATION, LOCATION, etc.)")
    confidence: float = Field(description="Confidence score (0.0 to 1.0)", ge=0.0, le=1.0)


class EntityExtractionOutput(BaseModel):
    """Output model for entity extraction."""

    entities: list[ExtractedEntity] = Field(description="List of extracted entities")


class ExtractedRelationship(BaseModel):
    """Model for a single extracted relationship."""

    entity1_name: str = Field(description="First entity name")
    entity2_name: str = Field(description="Second entity name")
    relationship_type: str = Field(description="Type of relationship")
    description: str = Field(description="Natural language description of the relationship")
    confidence: float = Field(description="Confidence score (0.0 to 1.0)", ge=0.0, le=1.0)


class RelationshipExtractionOutput(BaseModel):
    """Output model for relationship extraction."""

    relationships: list[ExtractedRelationship] = Field(description="List of extracted relationships")


# ============================================
# EXTRACTION TOOLS
# ============================================


class EntityExtractor:
    """
    Tool for extracting entities from text using LLM with structured output.
    """

    def __init__(self, llm: BaseChatModel) -> None:
        """
        Initialize the entity extractor.

        Args:
            llm: Language model
        """
        self.llm = llm

        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert at extracting named entities from text.

Extract all named entities from the provided text. Identify:
- PERSON: Names of people
- ORGANIZATION: Companies, institutions, organizations
- LOCATION: Places, cities, countries, addresses
- DATE: Dates, times, periods
- PRODUCT: Products, services, tools
- CONCEPT: Abstract concepts, theories, methods
- EVENT: Named events, meetings, conferences

For each entity, provide:
- name: The exact text as it appears
- type: One of the types above
- confidence: How confident you are (0.0 to 1.0)

Be thorough but precise. Only extract entities that are clearly identifiable.""",
                ),
                ("human", "Text to analyze:\n\n{text}"),
            ]
        )

        # Create structured output chain
        self.chain = self.prompt | self.llm.with_structured_output(EntityExtractionOutput)

    async def extract(self, text: str) -> list[dict[str, Any]]:
        """
        Extract entities from text.

        Args:
            text: Text to extract entities from

        Returns:
            List of extracted entities as dictionaries
        """
        try:
            result = await self.chain.ainvoke({"text": text})

            entities = []
            for entity in result.entities:
                entities.append(
                    {
                        "id": str(uuid4()),
                        "name": entity.name,
                        "type": entity.type,
                        "confidence": entity.confidence,
                        "extraction_method": "llm_structured",
                    }
                )

            logger.info(f"Extracted {len(entities)} entities from text")
            return entities

        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return []


class RelationshipExtractor:
    """
    Tool for extracting relationships between entities using LLM.
    """

    def __init__(self, llm: BaseChatModel) -> None:
        """
        Initialize the relationship extractor.

        Args:
            llm: Language model
        """
        self.llm = llm

        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert at identifying relationships between entities in text.

Given a list of entities extracted from a text, identify relationships between them based on the original text.

For each relationship, provide:
- entity1_name: Name of the first entity
- entity2_name: Name of the second entity
- relationship_type: Type of relationship (e.g., works_at, located_in, part_of, related_to)
- description: Natural language description of the relationship
- confidence: How confident you are (0.0 to 1.0)

Only extract relationships that are explicitly or strongly implied in the text.""",
                ),
                (
                    "human",
                    """Original text:
{text}

Entities found:
{entities}

Identify relationships between these entities based on the text.""",
                ),
            ]
        )

        # Create structured output chain
        self.chain = self.prompt | self.llm.with_structured_output(RelationshipExtractionOutput)

    async def extract(self, text: str, entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Extract relationships between entities.

        Args:
            text: Original text
            entities: List of extracted entities

        Returns:
            List of extracted relationships as dictionaries
        """
        if len(entities) < 2:
            logger.info("Not enough entities to extract relationships")
            return []

        try:
            # Format entities for prompt
            entity_list = "\n".join(
                [f"- {e['name']} ({e['type']})" for e in entities[:50]]  # Limit to first 50
            )

            result = await self.chain.ainvoke({"text": text, "entities": entity_list})

            relationships = []
            for rel in result.relationships:
                relationships.append(
                    {
                        "entity1_name": rel.entity1_name,
                        "entity2_name": rel.entity2_name,
                        "relationship_type": rel.relationship_type,
                        "description": rel.description,
                        "confidence": rel.confidence,
                    }
                )

            logger.info(f"Extracted {len(relationships)} relationships")
            return relationships

        except Exception as e:
            logger.error(f"Relationship extraction failed: {e}")
            return []
