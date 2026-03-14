"""
FastAPI application entry point
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from anthropic import APIError, RateLimitError
from sqlalchemy.exc import SQLAlchemyError
from api.config import CORS_ORIGINS, API_PREFIX, LOG_LEVEL
from api.core.database import init_db

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("Starting up application...")
    await init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title="Computer Use API",
    description="API for Claude Computer Use with session management and streaming",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Computer Use API",
        "version": "0.1.0",
        "docs": "/docs"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled exceptions
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "type": exc.__class__.__name__
        }
    )


# Claude API error handler
@app.exception_handler(RateLimitError)
async def rate_limit_handler(request: Request, exc: RateLimitError):
    """
    Handle Claude API rate limit errors
    """
    logger.warning(f"Rate limit error: {exc}")
    retry_after = exc.response.headers.get("retry-after", "unknown")
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "detail": str(exc),
            "retry_after": retry_after
        }
    )


@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    """
    Handle Claude API errors
    """
    logger.error(f"Claude API error: {exc}")
    return JSONResponse(
        status_code=502,
        content={
            "error": "Claude API error",
            "detail": str(exc),
            "type": exc.__class__.__name__
        }
    )


# Database error handler
@app.exception_handler(SQLAlchemyError)
async def database_error_handler(request: Request, exc: SQLAlchemyError):
    """
    Handle database errors
    """
    logger.error(f"Database error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Database error",
            "detail": "An error occurred while accessing the database"
        }
    )


# Import and include routers
from api.routes import sessions, messages, health, streaming

app.include_router(sessions.router, prefix=API_PREFIX)
app.include_router(messages.router, prefix=API_PREFIX)
app.include_router(health.router, prefix=API_PREFIX)
app.include_router(streaming.router, prefix=API_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
