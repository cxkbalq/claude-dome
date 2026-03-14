#!/usr/bin/env python3
"""
Test script to verify streaming output functionality
"""
import asyncio
import json
import httpx
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

async def test_streaming():
    """Test the streaming endpoint"""
    
    # Create a session
    print("Creating session...")
    async with httpx.AsyncClient() as client:
        session_response = await client.post(
            f"{API_BASE_URL}/sessions",
            json={
                "model": "claude-3-5-sonnet-20241022",
                "provider": "anthropic",
                "api_key": "sk-test",  # Replace with actual key
                "streaming": True
            }
        )
        session_data = session_response.json()
        session_id = session_data["id"]
        print(f"Session created: {session_id}")
        
        # Connect to SSE stream
        print("\nConnecting to SSE stream...")
        async with client.stream("GET", f"{API_BASE_URL}/sessions/{session_id}/stream") as response:
            print(f"SSE connection status: {response.status_code}")
            
            # Send a message
            print("\nSending message...")
            message_response = await client.post(
                f"{API_BASE_URL}/sessions/{session_id}/messages",
                json={"content": "Hello, what is 2+2?"}
            )
            print(f"Message sent: {message_response.json()}")
            
            # Read SSE events
            print("\nReading SSE events...")
            event_count = 0
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    event_count += 1
                    try:
                        data = json.loads(line[6:])  # Remove "data: " prefix
                        print(f"Event {event_count}: {data.get('type')} - {str(data.get('content', ''))[:100]}")
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse event: {e}")
                elif line.startswith(":"):
                    print(f"Heartbeat received")
            
            print(f"\nTotal events received: {event_count}")

if __name__ == "__main__":
    asyncio.run(test_streaming())
