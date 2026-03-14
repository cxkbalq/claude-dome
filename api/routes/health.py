"""
Health check routes
"""

from fastapi import APIRouter
from datetime import datetime


router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "computer-use-api"
    }
