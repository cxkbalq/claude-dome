"""
Message routes
"""

import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.core.database import get_db_session
from api.services import session_service, message_service


router = APIRouter(prefix="/sessions/{session_id}/messages", tags=["messages"])


class SendMessageRequest(BaseModel):
    """Send message request"""
    message: str


class SendMessageResponse(BaseModel):
    """Send message response"""
    message_id: int
    session_id: str


@router.post("", response_model=SendMessageResponse)
async def send_message(session_id: str, request: SendMessageRequest):
    """
    Send a message to a session
    This endpoint adds the user message to the database.
    Use the /stream endpoint to get the assistant's response.
    """
    async with get_db_session() as db:
        # Check if session exists
        session = await session_service.get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Add user message
        message = await message_service.add_message(
            db,
            session_id=session_id,
            role="user",
            content=[{"type": "text", "text": request.message}]
        )
        
        # Update session timestamp
        await session_service.update_session_timestamp(db, session_id)
        
        return SendMessageResponse(
            message_id=message.id,
            session_id=session_id
        )
