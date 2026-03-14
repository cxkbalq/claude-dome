"""
Session management routes
"""

import json
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from api.core.database import get_db_session
from api.services import session_service, message_service
from api.core.session_manager import session_manager


router = APIRouter(prefix="/sessions", tags=["sessions"])


class SessionConfig(BaseModel):
    """Session configuration"""
    model: str = "claude-sonnet-4-5-20250929"
    provider: str = "anthropic"
    api_key: str
    system_prompt: str = ""
    max_tokens: int = 16384
    thinking_budget: int | None = None
    tool_version: str = "computer_use_20250124"
    only_n_most_recent_images: int = 3
    token_efficient_tools_beta: bool = False


class SessionResponse(BaseModel):
    """Session response"""
    id: str
    created_at: str
    updated_at: str
    config: dict


class MessageResponse(BaseModel):
    """Message response"""
    id: int
    session_id: str
    role: str
    content: dict | list
    created_at: str


class SessionDetailResponse(BaseModel):
    """Session detail with messages"""
    id: str
    created_at: str
    updated_at: str
    config: dict
    messages: List[MessageResponse]


@router.post("", response_model=SessionResponse)
async def create_session(config: SessionConfig):
    """
    Create a new session
    """
    async with get_db_session() as db:
        session = await session_service.create_session(
            db,
            config.model_dump()
        )
        
        return SessionResponse(
            id=session.id,
            created_at=session.created_at.isoformat(),
            updated_at=session.updated_at.isoformat(),
            config=json.loads(session.config)
        )


@router.get("", response_model=List[SessionResponse])
async def list_sessions(limit: int = 100, offset: int = 0):
    """
    List all sessions
    """
    async with get_db_session() as db:
        sessions = await session_service.list_sessions(db, limit, offset)
        
        return [
            SessionResponse(
                id=s.id,
                created_at=s.created_at.isoformat(),
                updated_at=s.updated_at.isoformat(),
                config=json.loads(s.config)
            )
            for s in sessions
        ]


@router.get("/{session_id}", response_model=SessionDetailResponse)
async def get_session(session_id: str):
    """
    Get session details with messages
    """
    async with get_db_session() as db:
        session = await session_service.get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        messages = await message_service.get_messages(db, session_id)
        
        return SessionDetailResponse(
            id=session.id,
            created_at=session.created_at.isoformat(),
            updated_at=session.updated_at.isoformat(),
            config=json.loads(session.config),
            messages=[
                MessageResponse(
                    id=m.id,
                    session_id=m.session_id,
                    role=m.role,
                    content=json.loads(m.content),
                    created_at=m.created_at.isoformat()
                )
                for m in messages
            ]
        )


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session
    """
    async with get_db_session() as db:
        deleted = await session_service.delete_session(db, session_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Clean up session lock
        session_manager.cleanup_lock(session_id)
        
        return {"message": "Session deleted successfully"}
