"""
Health check endpoints.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Depends

from packages.shared.config import get_settings
from packages.shared.database import DatabasePool, get_db_pool
from packages.shared.models import HealthCheckResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check(
    db_pool: DatabasePool = Depends(get_db_pool),
) -> HealthCheckResponse:
    """
    Health check endpoint.

    Returns:
        Health status of the application
    """
    settings = get_settings()

    # Check database connection
    db_healthy = False
    graph_healthy = False

    try:
        # Test basic database query
        await db_pool.fetchval("SELECT 1")
        db_healthy = True

        # Test AGE graph query
        result = await db_pool.execute_cypher(
            settings.graph_name, "MATCH (n) RETURN count(n) LIMIT 1"
        )
        graph_healthy = True

    except Exception as e:
        logger.error(f"Health check failed: {e}")

    status = "healthy" if (db_healthy and graph_healthy) else "unhealthy"

    return HealthCheckResponse(
        status=status,
        version=settings.app_version,
        database=db_healthy,
        graph=graph_healthy,
        timestamp=datetime.utcnow(),
    )
