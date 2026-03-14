"""
Message persistence service
"""

import json
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.message import Message


async def add_message(
    db: AsyncSession,
    session_id: str,
    role: str,
    content: dict | list
) -> Message:
    """
    Add a message to a session
    
    Args:
        db: Database session
        session_id: Session ID
        role: Message role ('user', 'assistant', 'tool')
        content: Message content (will be serialized to JSON)
        
    Returns:
        Created message object
    """
    content_json = json.dumps(content, ensure_ascii=False)
    
    new_message = Message(
        session_id=session_id,
        role=role,
        content=content_json,
        created_at=datetime.utcnow()
    )
    
    db.add(new_message)
    await db.flush()
    await db.refresh(new_message)
    
    return new_message


async def get_messages(
    db: AsyncSession,
    session_id: str,
    limit: Optional[int] = None,
    offset: int = 0
) -> List[Message]:
    """
    Get messages for a session ordered by created_at
    
    Args:
        db: Database session
        session_id: Session ID
        limit: Maximum number of messages to return
        offset: Number of messages to skip
        
    Returns:
        List of message objects ordered by created_at ascending
    """
    query = select(Message).where(
        Message.session_id == session_id
    ).order_by(Message.created_at.asc())
    
    if limit is not None:
        query = query.limit(limit)
    
    query = query.offset(offset)
    
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_message_count(db: AsyncSession, session_id: str) -> int:
    """
    Get the count of messages in a session
    
    Args:
        db: Database session
        session_id: Session ID
        
    Returns:
        Number of messages
    """
    from sqlalchemy import func
    result = await db.execute(
        select(func.count(Message.id)).where(Message.session_id == session_id)
    )
    return result.scalar() or 0
