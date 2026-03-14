"""
Reset database - drops all tables and recreates them
"""

import asyncio
import logging
from api.core.database import engine, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def reset_db():
    """
    Drop all tables and recreate them
    """
    logger.info("Dropping all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    logger.info("Creating all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database reset complete!")


if __name__ == "__main__":
    asyncio.run(reset_db())