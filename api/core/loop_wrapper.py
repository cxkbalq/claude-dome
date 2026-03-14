"""
Wrapper for computer_use_demo.loop.sampling_loop
Adapts the sampling loop for SSE streaming
"""

import sys
from pathlib import Path
from typing import Callable, Awaitable, Any
from anthropic.types.beta import BetaMessageParam, BetaContentBlockParam
import httpx

# Add parent directory to path to import computer_use_demo
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from computer_use_demo.loop import sampling_loop, APIProvider
from computer_use_demo.tools import ToolResult, ToolVersion


class ConversationEngine:
    """
    Wrapper for the sampling loop with SSE-compatible callbacks
    """
    
    def __init__(self):
        self.current_session_id = None
    
    async def process_conversation(
        self,
        *,
        session_id: str,
        model: str,
        provider: str,
        api_key: str,
        messages: list[BetaMessageParam],
        system_prompt_suffix: str = "",
        max_tokens: int = 16384,
        thinking_budget: int | None = None,
        tool_version: ToolVersion = "computer_use_20250124",
        only_n_most_recent_images: int = 3,
        token_efficient_tools_beta: bool = False,
        output_callback: Callable[[BetaContentBlockParam], Awaitable[None]] | None = None,
        tool_output_callback: Callable[[ToolResult, str], Awaitable[None]] | None = None,
        api_response_callback: Callable[[httpx.Request, httpx.Response | object | None, Exception | None], Awaitable[None]] | None = None,
    ) -> list[BetaMessageParam]:
        """
        Process a conversation using the sampling loop
        
        Args:
            session_id: Session ID for tracking
            model: Model name
            provider: API provider ('anthropic', 'bedrock', 'vertex')
            api_key: API key
            messages: Conversation messages
            system_prompt_suffix: Additional system prompt
            max_tokens: Maximum output tokens
            thinking_budget: Thinking budget tokens
            tool_version: Tool version to use
            only_n_most_recent_images: Number of recent images to keep
            token_efficient_tools_beta: Enable token-efficient tools beta
            output_callback: Callback for output content
            tool_output_callback: Callback for tool results
            api_response_callback: Callback for API responses
            
        Returns:
            Updated messages list
        """
        self.current_session_id = session_id
        
        # Default callbacks if not provided
        if output_callback is None:
            async def output_callback(content):
                pass
        
        if tool_output_callback is None:
            async def tool_output_callback(result, tool_id):
                pass
        
        if api_response_callback is None:
            async def api_response_callback(request, response, error):
                pass
        
        # Convert provider string to enum
        api_provider = APIProvider(provider)
        
        # Call the sampling loop
        updated_messages = await sampling_loop(
            model=model,
            provider=api_provider,
            system_prompt_suffix=system_prompt_suffix,
            messages=messages,
            output_callback=output_callback,
            tool_output_callback=tool_output_callback,
            api_response_callback=api_response_callback,
            api_key=api_key,
            only_n_most_recent_images=only_n_most_recent_images,
            max_tokens=max_tokens,
            tool_version=tool_version,
            thinking_budget=thinking_budget,
            token_efficient_tools_beta=token_efficient_tools_beta,
            streaming=False,  # Use non-streaming for compatibility
        )
        
        return updated_messages
