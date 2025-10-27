"""
Objectives CRUD endpoints.
"""

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from packages.shared.config import get_settings
from packages.shared.database import DatabasePool, get_db_pool
from packages.shared.models import (
    ObjectiveCreate,
    ObjectiveResponse,
    ObjectiveStats,
    ObjectiveStatus,
    ObjectiveUpdate,
)
from packages.shared.repositories import ObjectivesRepository

logger = logging.getLogger(__name__)

router = APIRouter()


def get_objectives_repo(
    db_pool: DatabasePool = Depends(get_db_pool),
) -> ObjectivesRepository:
    """
    Dependency for getting objectives repository.

    Returns:
        ObjectivesRepository instance
    """
    return ObjectivesRepository(db_pool)


@router.post("/objectives", response_model=ObjectiveResponse, status_code=201)
async def create_objective(
    objective: ObjectiveCreate,
    repo: ObjectivesRepository = Depends(get_objectives_repo),
) -> ObjectiveResponse:
    """
    Create a new objective.

    Args:
        objective: Objective creation data

    Returns:
        Created objective
    """
    try:
        # Check if name already exists
        existing = await repo.get_by_name(objective.name)
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Objective with name '{objective.name}' already exists",
            )

        # Create objective
        data = objective.model_dump()
        data["status"] = ObjectiveStatus.DRAFT.value
        record = await repo.create(data)

        return ObjectiveResponse(**dict(record))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create objective: {e}")
        raise HTTPException(status_code=500, detail="Failed to create objective")


@router.get("/objectives", response_model=list[ObjectiveResponse])
async def list_objectives(
    status: Optional[ObjectiveStatus] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    repo: ObjectivesRepository = Depends(get_objectives_repo),
) -> list[ObjectiveResponse]:
    """
    List objectives with optional filtering.

    Args:
        status: Filter by status
        limit: Maximum number of results
        offset: Number of results to skip

    Returns:
        List of objectives
    """
    try:
        if status:
            records = await repo.list_by_status(status.value, limit, offset)
        else:
            records = await repo.get_all(limit, offset)

        return [ObjectiveResponse(**dict(record)) for record in records]

    except Exception as e:
        logger.error(f"Failed to list objectives: {e}")
        raise HTTPException(status_code=500, detail="Failed to list objectives")


@router.get("/objectives/{objective_id}", response_model=ObjectiveResponse)
async def get_objective(
    objective_id: UUID,
    repo: ObjectivesRepository = Depends(get_objectives_repo),
) -> ObjectiveResponse:
    """
    Get an objective by ID.

    Args:
        objective_id: Objective UUID

    Returns:
        Objective details
    """
    try:
        record = await repo.get_by_id(objective_id)
        if not record:
            raise HTTPException(status_code=404, detail="Objective not found")

        return ObjectiveResponse(**dict(record))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get objective: {e}")
        raise HTTPException(status_code=500, detail="Failed to get objective")


@router.put("/objectives/{objective_id}", response_model=ObjectiveResponse)
async def update_objective(
    objective_id: UUID,
    objective: ObjectiveUpdate,
    repo: ObjectivesRepository = Depends(get_objectives_repo),
) -> ObjectiveResponse:
    """
    Update an objective.

    Args:
        objective_id: Objective UUID
        objective: Update data

    Returns:
        Updated objective
    """
    try:
        # Check if exists
        existing = await repo.get_by_id(objective_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Objective not found")

        # Check name uniqueness if changing name
        if objective.name and objective.name != existing["name"]:
            name_exists = await repo.get_by_name(objective.name)
            if name_exists:
                raise HTTPException(
                    status_code=400,
                    detail=f"Objective with name '{objective.name}' already exists",
                )

        # Update objective
        data = objective.model_dump(exclude_unset=True)
        record = await repo.update(objective_id, data)

        return ObjectiveResponse(**dict(record))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update objective: {e}")
        raise HTTPException(status_code=500, detail="Failed to update objective")


@router.delete("/objectives/{objective_id}", status_code=204)
async def delete_objective(
    objective_id: UUID,
    repo: ObjectivesRepository = Depends(get_objectives_repo),
) -> None:
    """
    Delete an objective.

    Args:
        objective_id: Objective UUID
    """
    try:
        deleted = await repo.delete(objective_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Objective not found")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete objective: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete objective")


@router.get("/objectives/{objective_id}/stats", response_model=ObjectiveStats)
async def get_objective_stats(
    objective_id: UUID,
    repo: ObjectivesRepository = Depends(get_objectives_repo),
) -> ObjectiveStats:
    """
    Get statistics for an objective.

    Args:
        objective_id: Objective UUID

    Returns:
        Objective statistics
    """
    try:
        # Check if objective exists
        objective = await repo.get_by_id(objective_id)
        if not objective:
            raise HTTPException(status_code=404, detail="Objective not found")

        # Get stats
        record = await repo.get_stats(objective_id)
        if not record:
            raise HTTPException(status_code=404, detail="Statistics not found")

        return ObjectiveStats(**dict(record))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get objective stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get objective stats")
