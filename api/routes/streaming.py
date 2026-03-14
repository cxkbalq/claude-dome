"""
SSE streaming routes
"""

import asyncio
import json
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from anthropic.types.beta import BetaTextBlockParam
from api.core.database import get_db_session
from api.services import session_service, message_service
from api.core.session_manager import session_manager
from computer_use_demo.tools import ToolResult


router = APIRouter(prefix="/sessions/{session_id}", tags=["streaming"])
logger = logging.getLogger(__name__)



@router.get("/stream")
async def stream_conversation(session_id: str):
    """
    Stream conversation responses using Server-Sent Events (SSE)
    """
    # Verify session exists and get config
    async with get_db_session() as db:
        session = await session_service.get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        config = json.loads(session.config)
        
        # Get existing messages
        messages_db = await message_service.get_messages(db, session_id)
        
        # Convert to API format
        messages = []
        for msg in messages_db:
            content = json.loads(msg.content)
            messages.append({
                "role": msg.role,
                "content": content
            })
    
    async def event_generator():
        """Generate SSE events"""
        try:
            # Collect all content
            collected_content = []
            collected_tool_results = []
            
            def make_output_callback():
                """Create output callback that collects content"""
                async def output_callback(content):
                    collected_content.append(content)
                return output_callback
            
            def make_tool_output_callback():
                """Create tool callback that collects results"""
                async def tool_callback(result: ToolResult, tool_id: str):
                    collected_tool_results.append({
                        "tool_id": tool_id,
                        "output": result.output,
                        "error": result.error,
                        "base64_image": result.base64_image
                    })
                return tool_callback
            
            def make_api_callback():
                """Create API callback"""
                async def api_callback(request, response, error):
                    if error:
                        logger.error(f"API error: {error}")
                return api_callback
            
            # Process conversation
            updated_messages = await session_manager.process_message(
                session_id=session_id,
                model=config.get("model", "claude-sonnet-4-5-20250929"),
                provider=config.get("provider", "anthropic"),
                api_key=config["api_key"],
                messages=messages,
                system_prompt_suffix=config.get("system_prompt", ""),
                max_tokens=config.get("max_tokens", 16384),
                thinking_budget=config.get("thinking_budget"),
                tool_version=config.get("tool_version", "computer_use_20250124"),
                only_n_most_recent_images=config.get("only_n_most_recent_images", 3),
                token_efficient_tools_beta=config.get("token_efficient_tools_beta", False),
                output_callback=make_output_callback(),
                tool_output_callback=make_tool_output_callback(),
                api_response_callback=make_api_callback(),
            )
            
            for content in collected_content:
                if content.get("type") == "text" and content.get("text"):
                    text = content["text"]
                    for i in range(0, len(text), STREAMING_MIN_CHUNK_SIZE):
                        chunk = text[i:i + STREAMING_MIN_CHUNK_SIZE]
                        event_data = {
                            "event": "content",
                            "data": {
                                "type": "text",
                                "text": chunk,
                                "partial": True
                            }
                        }
                        yield f"data: {json.dumps(event_data)}\n\n"
                        await asyncio.sleep(STREAMING_CHUNK_DELAY)
                    
                    # 发送完成标记
                    event_data = {
                        "event": "content",
                        "data": {
                            "type": "text",
                            "text": "",
                            "partial": False
                        }
                    }
                    yield f"data: {json.dumps(event_data)}\n\n"
                else:
                    # 非文本内容（如 thinking、tool_use 等）直接发送
                    event_data = {"event": "content", "data": content}
                    yield f"data: {json.dumps(event_data)}\n\n"
                    await asyncio.sleep(STREAMING_CHUNK_DELAY)
            
            # Send collected tool results through SSE
            for tool_data in collected_tool_results:
                event_data = {"event": "tool_result", "data": tool_data}
                yield f"data: {json.dumps(event_data)}\n\n"
            
            # Save new messages to database
            async with get_db_session() as db:
                # Find new messages (after the original message count)
                original_count = len(messages)
                new_messages = updated_messages[original_count:]
                
                for msg in new_messages:
                    await message_service.add_message(
                        db,
                        session_id=session_id,
                        role=msg["role"],
                        content=msg["content"]
                    )
                
                # Update session timestamp
                await session_service.update_session_timestamp(db, session_id)
            
            # Send complete event
            yield f"data: {json.dumps({'event': 'complete'})}\n\n"
            
        except Exception as e:
            logger.error(f"Streaming error: {e}", exc_info=True)
            error_data = {"event": "error", "data": {"message": str(e)}}
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
