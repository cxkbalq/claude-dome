"""
Session management service
"""

import json
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.session import Session
from api.models.message import Message


async def create_session(db: AsyncSession, config: dict) -> Session:
    """
    Create a new session with unique ID
    
    Args:
        db: Database session
        config: Session configuration dictionary
        
    Returns:
        Created session object
    """
    session_id = str(uuid.uuid4())
    config_json = json.dumps(config)
    
    new_session = Session(
        id=session_id,
        config=config_json,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(new_session)
    await db.flush()
    await db.refresh(new_session)
    
    return new_session


async def get_session(db: AsyncSession, session_id: str) -> Optional[Session]:
    """
    Get a session by ID
    
    Args:
        db: Database session
        session_id: Session ID
        
    Returns:
        Session object or None if not found
    """
    result = await db.execute(
        select(Session).where(Session.id == session_id)
    )
    return result.scalar_one_or_none()


async def list_sessions(db: AsyncSession, limit: int = 100, offset: int = 0) -> List[Session]:
    """
    List all sessions ordered by updated_at descending
    
    Args:
        db: Database session
        limit: Maximum number of sessions to return
        offset: Number of sessions to skip
        
    Returns:
        List of session objects
    """
    result = await db.execute(
        select(Session)
        .order_by(Session.updated_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all())


async def delete_session(db: AsyncSession, session_id: str) -> bool:
    """
    Delete a session and all associated messages (cascade)
    
    Args:
        db: Database session
        session_id: Session ID
        
    Returns:
        True if session was deleted, False if not found
    """
    result = await db.execute(
        delete(Session).where(Session.id == session_id)
    )
    return result.rowcount > 0


async def update_session_timestamp(db: AsyncSession, session_id: str) -> None:
    """
    Update session's updated_at timestamp
    
    Args:
        db: Database session
        session_id: Session ID
    """
    session = await get_session(db, session_id)
    if session:
        session.updated_at = datetime.utcnow()
        await db.flush()
