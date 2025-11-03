"""
Sources CRUD endpoints.
"""

import logging
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query

from packages.agents.extraction_agent import ExtractionAgent
from packages.shared.database import DatabasePool, get_db_pool
from packages.shared.models import (
    ExtractionStatus,
    ExtractionStatusResponse,
    SourceCreate,
    SourceResponse,
)
from packages.shared.repositories import ObjectivesRepository
from packages.shared.repositories.sources import SourcesRepository

logger = logging.getLogger(__name__)

router = APIRouter()


async def run_extraction_task(source_id: UUID, db_pool: DatabasePool) -> None:
    """
    Background task that executes extraction on a source document.

    Args:
        source_id: Source UUID to extract
        db_pool: Database connection pool
    """
    try:
        logger.info(f"Starting extraction task for source {source_id}")

        agent = ExtractionAgent(db_pool)

        state = {
            "source_id": source_id,
            "agent_path": [],
            "errors": [],
            "retry_count": 0,
        }

        result_state = await agent.execute(state)

        if result_state.get("errors"):
            logger.warning(f"Extraction completed with errors: {result_state['errors']}")
        else:
            logger.info(f"Extraction task completed successfully for source {source_id}")

    except Exception as e:
        logger.error(f"Extraction task failed for source {source_id}: {e}", exc_info=True)

        try:
            sources_repo = SourcesRepository(db_pool)
            await sources_repo.update_extraction_status(
                source_id,
                ExtractionStatus.FAILED.value,
                error=str(e)
            )
        except Exception as update_error:
            logger.error(f"Failed to update extraction status: {update_error}")


def get_sources_repo(
    db_pool: DatabasePool = Depends(get_db_pool),
) -> SourcesRepository:
    """
    Dependency for getting sources repository.

    Returns:
        SourcesRepository instance
    """
    return SourcesRepository(db_pool)


def get_objectives_repo(
    db_pool: DatabasePool = Depends(get_db_pool),
) -> ObjectivesRepository:
    """
    Dependency for getting objectives repository.

    Returns:
        ObjectivesRepository instance
    """
    return ObjectivesRepository(db_pool)


@router.post(
    "/objectives/{objective_id}/sources",
    response_model=SourceResponse,
    status_code=201,
)
async def create_source(
    objective_id: UUID,
    source: SourceCreate,
    sources_repo: SourcesRepository = Depends(get_sources_repo),
    objectives_repo: ObjectivesRepository = Depends(get_objectives_repo),
) -> SourceResponse:
    """
    Upload a text document as a source for an objective.

    Args:
        objective_id: Objective UUID
        source: Source creation data

    Returns:
        Created source
    """
    try:
        # Check if objective exists
        objective = await objectives_repo.get_by_id(objective_id)
        if not objective:
            raise HTTPException(status_code=404, detail="Objective not found")

        # Check if source name already exists for this objective
        existing = await sources_repo.get_by_objective_and_name(objective_id, source.name)
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Source with name '{source.name}' already exists for this objective",
            )

        # Create source
        data = source.model_dump()
        data["objective_id"] = objective_id
        data["content_type"] = "text"
        data["extraction_status"] = ExtractionStatus.PENDING.value
        data["extraction_progress"] = {}

        record = await sources_repo.create(data)
        return SourceResponse(**dict(record))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create source: {e}")
        raise HTTPException(status_code=500, detail="Failed to create source")


@router.get("/objectives/{objective_id}/sources", response_model=list[SourceResponse])
async def list_sources(
    objective_id: UUID,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    sources_repo: SourcesRepository = Depends(get_sources_repo),
    objectives_repo: ObjectivesRepository = Depends(get_objectives_repo),
) -> list[SourceResponse]:
    """
    List all sources for an objective.

    Args:
        objective_id: Objective UUID
        limit: Maximum number of results
        offset: Number of results to skip

    Returns:
        List of sources
    """
    try:
        # Check if objective exists
        objective = await objectives_repo.get_by_id(objective_id)
        if not objective:
            raise HTTPException(status_code=404, detail="Objective not found")

        records = await sources_repo.get_by_objective(objective_id, limit, offset)
        return [SourceResponse(**dict(record)) for record in records]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to list sources: {e}")
        raise HTTPException(status_code=500, detail="Failed to list sources")


@router.get("/sources/{source_id}", response_model=SourceResponse)
async def get_source(
    source_id: UUID,
    sources_repo: SourcesRepository = Depends(get_sources_repo),
) -> SourceResponse:
    """
    Get a source by ID.

    Args:
        source_id: Source UUID

    Returns:
        Source details
    """
    try:
        record = await sources_repo.get_by_id(source_id)
        if not record:
            raise HTTPException(status_code=404, detail="Source not found")

        return SourceResponse(**dict(record))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get source: {e}")
        raise HTTPException(status_code=500, detail="Failed to get source")


@router.delete("/sources/{source_id}", status_code=204)
async def delete_source(
    source_id: UUID,
    sources_repo: SourcesRepository = Depends(get_sources_repo),
) -> None:
    """
    Delete a source.

    Args:
        source_id: Source UUID
    """
    try:
        deleted = await sources_repo.delete(source_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Source not found")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete source: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete source")


@router.post("/sources/{source_id}/extract", status_code=202)
async def trigger_extraction(
    source_id: UUID,
    background_tasks: BackgroundTasks,
    sources_repo: SourcesRepository = Depends(get_sources_repo),
    db_pool: DatabasePool = Depends(get_db_pool),
) -> dict:
    """
    Trigger extraction for a source.

    Args:
        source_id: Source UUID
        background_tasks: FastAPI background tasks manager
        sources_repo: Sources repository
        db_pool: Database connection pool

    Returns:
        Extraction trigger confirmation
    """
    try:
        source = await sources_repo.get_by_id(source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")

        await sources_repo.update_extraction_status(
            source_id, ExtractionStatus.PROCESSING.value, {"current_stage": "initializing"}
        )

        background_tasks.add_task(run_extraction_task, source_id, db_pool)

        return {
            "message": "Extraction triggered",
            "source_id": str(source_id),
            "status": "PROCESSING",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to trigger extraction: {e}")
        raise HTTPException(status_code=500, detail="Failed to trigger extraction")


@router.get("/sources/{source_id}/extraction-status", response_model=ExtractionStatusResponse)
async def get_extraction_status(
    source_id: UUID,
    sources_repo: SourcesRepository = Depends(get_sources_repo),
) -> ExtractionStatusResponse:
    """
    Get extraction status for a source.

    Args:
        source_id: Source UUID

    Returns:
        Extraction status information
    """
    try:
        source = await sources_repo.get_by_id(source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")

        from packages.shared.models import ExtractionProgress

        return ExtractionStatusResponse(
            source_id=source_id,
            status=ExtractionStatus(source["extraction_status"]),
            progress=ExtractionProgress(**source["extraction_progress"]),
            error=source["extraction_error"],
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get extraction status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get extraction status")
