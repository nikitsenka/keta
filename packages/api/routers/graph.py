"""
Graph knowledge base endpoints.
"""

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from packages.graph.repository import KnowledgeGraphRepository
from packages.shared.database import DatabasePool, get_db_pool
from packages.shared.models import (
    EntityResponse,
    EntityType,
    GraphStats,
    GraphVisualizationData,
    GraphVisualizationEdge,
    GraphVisualizationNode,
)
from packages.shared.repositories import SourcesRepository

logger = logging.getLogger(__name__)

router = APIRouter()


def get_graph_repo(
    db_pool: DatabasePool = Depends(get_db_pool),
) -> KnowledgeGraphRepository:
    return KnowledgeGraphRepository(db_pool)


def get_sources_repo(
    db_pool: DatabasePool = Depends(get_db_pool),
) -> SourcesRepository:
    return SourcesRepository(db_pool)


@router.get("/graph/entities", response_model=list[EntityResponse])
async def search_entities(
    objective_id: UUID,
    name: Optional[str] = Query(None, description="Search by entity name"),
    entity_type: Optional[EntityType] = Query(None, description="Filter by entity type"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of entities"),
    graph_repo: KnowledgeGraphRepository = Depends(get_graph_repo),
    sources_repo: SourcesRepository = Depends(get_sources_repo),
) -> list[EntityResponse]:
    try:
        sources = await sources_repo.get_by_objective(objective_id)
        source_ids = [str(s['id']) for s in sources]

        if not source_ids:
            return []

        where_clauses = [f"'{sid}' IN e.source_ids" for sid in source_ids]
        where_condition = " OR ".join(where_clauses)

        if name:
            safe_name = name.replace("'", "\\'")
            where_condition = f"({where_condition}) AND e.name CONTAINS '{safe_name}'"

        if entity_type:
            where_condition = f"({where_condition}) AND e.type = '{entity_type.value}'"

        cypher = f"""
            MATCH (e:Entity)
            WHERE {where_condition}
            RETURN e
            LIMIT {limit}
        """

        results = await graph_repo.execute_cypher(cypher)

        entities = []
        for result in results:
            entity_data = result if isinstance(result, dict) else {}
            try:
                entities.append(
                    EntityResponse(
                        id=UUID(entity_data["id"]),
                        name=entity_data["name"],
                        type=EntityType(entity_data["type"]),
                        source_ids=[UUID(sid) for sid in entity_data.get("source_ids", [])],
                        confidence=entity_data.get("confidence", 1.0),
                        extraction_method=entity_data.get("extraction_method", "unknown"),
                        created_at=entity_data["created_at"],
                        updated_at=entity_data["updated_at"],
                    )
                )
            except Exception as e:
                logger.error(f"Error parsing entity: {e}, data: {entity_data}")
                continue

        return entities

    except Exception as e:
        logger.error(f"Failed to search entities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/graph/entities/{entity_id}/neighborhood", response_model=GraphVisualizationData)
async def get_entity_neighborhood(
    entity_id: UUID,
    depth: int = Query(1, ge=1, le=3, description="Traversal depth"),
    graph_repo: KnowledgeGraphRepository = Depends(get_graph_repo),
) -> GraphVisualizationData:
    try:
        center_cypher = f"""
            MATCH (center:Entity {{id: '{entity_id}'}})
            RETURN center
        """

        center_results = await graph_repo.execute_cypher(center_cypher)

        if not center_results:
            raise HTTPException(status_code=404, detail="Entity not found")

        nodes = []
        edges = []
        node_ids = set()

        center = center_results[0]
        nodes.append(
            GraphVisualizationNode(
                id=center["id"],
                label=center["name"],
                type=center["type"],
                properties={
                    "confidence": center.get("confidence", 1.0),
                    "source_ids": center.get("source_ids", []),
                },
            )
        )
        node_ids.add(center["id"])

        neighbors_cypher = f"""
            MATCH (center:Entity {{id: '{entity_id}'}})-[:RELATED_TO*1..{depth}]-(connected:Entity)
            RETURN DISTINCT connected
        """

        connected_results = await graph_repo.execute_cypher(neighbors_cypher)
        for entity in connected_results:
            if entity and entity["id"] not in node_ids:
                nodes.append(
                    GraphVisualizationNode(
                        id=entity["id"],
                        label=entity["name"],
                        type=entity["type"],
                        properties={
                            "confidence": entity.get("confidence", 1.0),
                            "source_ids": entity.get("source_ids", []),
                        },
                    )
                )
                node_ids.add(entity["id"])

        all_node_ids = list(node_ids)
        for i, source_id in enumerate(all_node_ids):
            for target_id in all_node_ids[i+1:]:
                rel_check_cypher = f"""
                    MATCH (e1:Entity {{id: '{source_id}'}})-[r:RELATED_TO]-(e2:Entity {{id: '{target_id}'}})
                    RETURN r
                """

                rel_check_results = await graph_repo.execute_cypher(rel_check_cypher)
                for rel in rel_check_results:
                    if rel:
                        edges.append(
                            GraphVisualizationEdge(
                                source=source_id,
                                target=target_id,
                                label=rel.get("relationship_type", "RELATED_TO"),
                                properties={
                                    "description": rel.get("description", ""),
                                    "confidence": rel.get("confidence", 1.0),
                                },
                            )
                        )

        return GraphVisualizationData(nodes=nodes, edges=edges)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get entity neighborhood: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/graph/statistics/{objective_id}", response_model=GraphStats)
async def get_graph_statistics(
    objective_id: UUID,
    graph_repo: KnowledgeGraphRepository = Depends(get_graph_repo),
    sources_repo: SourcesRepository = Depends(get_sources_repo),
) -> GraphStats:
    try:
        sources = await sources_repo.get_by_objective(objective_id)
        source_ids = [str(s['id']) for s in sources]

        if not source_ids:
            return GraphStats(
                objective_id=objective_id,
                total_entities=0,
                total_relationships=0,
                entity_type_counts={},
                relationship_type_counts={},
            )

        where_clauses = [f"'{sid}' IN e.source_ids" for sid in source_ids]
        where_condition = " OR ".join(where_clauses)

        entity_counts_cypher = f"""
            MATCH (e:Entity)
            WHERE {where_condition}
            RETURN e
        """

        entity_results = await graph_repo.execute_cypher(entity_counts_cypher)
        entity_type_counts = {}
        for entity in entity_results:
            entity_type = entity.get('type', 'UNKNOWN')
            entity_type_counts[entity_type] = entity_type_counts.get(entity_type, 0) + 1
        total_entities = len(entity_results)

        where_rel_clauses = [f"'{sid}' IN r.source_ids" for sid in source_ids]
        where_rel_condition = " OR ".join(where_rel_clauses)

        rel_counts_cypher = f"""
            MATCH (e1:Entity)-[r:RELATED_TO]->(e2:Entity)
            WHERE {where_rel_condition}
            RETURN r
        """

        rel_results = await graph_repo.execute_cypher(rel_counts_cypher)
        relationship_type_counts = {}
        for rel in rel_results:
            rel_type = rel.get('relationship_type', 'UNKNOWN')
            relationship_type_counts[rel_type] = relationship_type_counts.get(rel_type, 0) + 1
        total_relationships = len(rel_results)

        return GraphStats(
            objective_id=objective_id,
            total_entities=total_entities,
            total_relationships=total_relationships,
            entity_type_counts=entity_type_counts,
            relationship_type_counts=relationship_type_counts,
        )

    except Exception as e:
        logger.error(f"Failed to get graph statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
