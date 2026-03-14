"""
Session manager with concurrency control
"""

import asyncio
from collections import defaultdict
from typing import Dict
from anthropic.types.beta import BetaMessageParam
from api.core.loop_wrapper import ConversationEngine


class SessionManager:
    """
    Manages conversation sessions with concurrency control
    """
    
    def __init__(self):
        self.locks: Dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)
        self.engine = ConversationEngine()
    
    async def process_message(
        self,
        session_id: str,
        **kwargs
    ) -> list[BetaMessageParam]:
        """
        Process a message with session-level locking to prevent race conditions
        
        Args:
            session_id: Session ID
            **kwargs: Arguments to pass to conversation engine
            
        Returns:
            Updated messages list
        """
        async with self.locks[session_id]:
            return await self.engine.process_conversation(
                session_id=session_id,
                **kwargs
            )
    
    def cleanup_lock(self, session_id: str):
        """
        Clean up lock for a session (call after session is deleted)
        
        Args:
            session_id: Session ID
        """
        if session_id in self.locks:
            del self.locks[session_id]


# Global session manager instance
session_manager = SessionManager()
