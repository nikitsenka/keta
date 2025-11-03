"""
KETA FastAPI Application.
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from packages.api.routers import objectives, sources, chat, health, graph
from packages.shared.config import get_settings
from packages.shared.database import db_pool
from packages.shared.models import ErrorResponse

# Get settings to configure logging
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.info(f"Logging configured with level: {settings.log_level.upper()}")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    logger.info("Starting KETA API...")

    # Initialize database pool
    try:
        await db_pool.initialize(
            database_url=settings.database_url,
            min_size=settings.db_pool_min_size,
            max_size=settings.db_pool_max_size,
        )
        logger.info("Database pool initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    yield

    # Cleanup
    logger.info("Shutting down KETA API...")
    await db_pool.close()
    logger.info("Database pool closed")


# Create FastAPI application
app = FastAPI(
    title="KETA API",
    description="Knowledge Extract & Talk Agent - Multi-agent POC",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(error="Bad Request", detail=str(exc)).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error",
            detail="An unexpected error occurred",
        ).model_dump(),
    )


# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(objectives.router, prefix=settings.api_prefix, tags=["Objectives"])
app.include_router(sources.router, prefix=settings.api_prefix, tags=["Sources"])
app.include_router(chat.router, prefix=settings.api_prefix, tags=["Chat"])
app.include_router(graph.router, prefix=settings.api_prefix, tags=["Graph"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "KETA API",
        "version": "0.1.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
    }
