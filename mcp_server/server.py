"""
Simple MCP Server for Futurama Quotes API
=========================================

A clean, working MCP server that connects to our Flask API.
"""

import asyncio
import json
import logging
from typing import Any, Dict

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
API_BASE_URL = "http://localhost:5000"
QUOTES_ENDPOINT = f"{API_BASE_URL}/api/quotes"
HEALTH_ENDPOINT = f"{API_BASE_URL}/health"

# HTTP client
httpx_client = httpx.Client()

app = Server("futurama-quotes-mcp-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="list_quotes",
            description="Get all Futurama quotes",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_quote",
            description="Get a specific quote by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "quote_id": {
                        "type": "integer",
                        "description": "The ID of the quote"
                    }
                },
                "required": ["quote_id"]
            }
        ),
        Tool(
            name="create_quote",
            description="Create a new quote",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Quote text"},
                    "character": {"type": "string", "description": "Character name"},
                    "episode": {"type": "string", "description": "Episode name"},
                    "season": {"type": "integer", "description": "Season number"},
                    "year": {"type": "integer", "description": "Year"}
                },
                "required": ["text", "character", "episode"]
            }
        ),
        Tool(
            name="update_quote",
            description="Update an existing quote",
            inputSchema={
                "type": "object",
                "properties": {
                    "quote_id": {
                        "type": "integer",
                        "description": "The ID of the quote to update"
                    },
                    "text": {"type": "string", "description": "Updated quote text"},
                    "character": {"type": "string", "description": "Updated character name"},
                    "episode": {"type": "string", "description": "Updated episode name"},
                    "season": {"type": "integer", "description": "Updated season number"},
                    "year": {"type": "integer", "description": "Updated year"}
                },
                "required": ["quote_id"]
            }
        ),
        Tool(
            name="delete_quote",
            description="Delete a quote by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "quote_id": {
                        "type": "integer",
                        "description": "The ID of the quote to delete"
                    }
                },
                "required": ["quote_id"]
            }
        ),
        Tool(
            name="health_check",
            description="Check API health",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    
    try:
        if name == "list_quotes":
            response = httpx_client.get(QUOTES_ENDPOINT)
            response.raise_for_status()
            data = response.json()
            
            result = f"Found {data['count']} quotes:\n\n"
            for quote in data['quotes']:
                result += f"ID {quote['id']}: \"{quote['text']}\" - {quote['character']}\n"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "get_quote":
            quote_id = arguments["quote_id"]
            response = httpx_client.get(f"{QUOTES_ENDPOINT}/{quote_id}")
            response.raise_for_status()
            quote = response.json()
            
            result = f"Quote ID {quote['id']}:\n"
            result += f"Text: \"{quote['text']}\"\n"
            result += f"Character: {quote['character']}\n"
            result += f"Episode: {quote['episode']}\n"
            if quote.get('season'):
                result += f"Season: {quote['season']}\n"
            if quote.get('year'):
                result += f"Year: {quote['year']}\n"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "create_quote":
            quote_data = {
                "text": arguments["text"],
                "character": arguments["character"],
                "episode": arguments["episode"]
            }
            if "season" in arguments:
                quote_data["season"] = arguments["season"]
            if "year" in arguments:
                quote_data["year"] = arguments["year"]
            
            response = httpx_client.post(QUOTES_ENDPOINT, json=quote_data)
            response.raise_for_status()
            quote = response.json()
            
            result = f"Created quote ID {quote['id']}:\n"
            result += f"Text: \"{quote['text']}\"\n"
            result += f"Character: {quote['character']}\n"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "update_quote":
            quote_id = arguments["quote_id"]
            quote_data = {}
            
            # Only include fields that are provided
            if "text" in arguments:
                quote_data["text"] = arguments["text"]
            if "character" in arguments:
                quote_data["character"] = arguments["character"]
            if "episode" in arguments:
                quote_data["episode"] = arguments["episode"]
            if "season" in arguments:
                quote_data["season"] = arguments["season"]
            if "year" in arguments:
                quote_data["year"] = arguments["year"]
            
            response = httpx_client.put(f"{QUOTES_ENDPOINT}/{quote_id}", json=quote_data)
            response.raise_for_status()
            quote = response.json()
            
            result = f"Updated quote ID {quote['id']}:\n"
            result += f"Text: \"{quote['text']}\"\n"
            result += f"Character: {quote['character']}\n"
            result += f"Episode: {quote['episode']}\n"
            if quote.get('season'):
                result += f"Season: {quote['season']}\n"
            if quote.get('year'):
                result += f"Year: {quote['year']}\n"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "delete_quote":
            quote_id = arguments["quote_id"]
            response = httpx_client.delete(f"{QUOTES_ENDPOINT}/{quote_id}")
            response.raise_for_status()
            data = response.json()
            
            result = f"Successfully deleted quote ID {quote_id}\n"
            result += f"Message: {data['message']}\n"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "health_check":
            response = httpx_client.get(HEALTH_ENDPOINT)
            response.raise_for_status()
            data = response.json()
            
            result = f"API Status: {data['status']}\n"
            result += f"Message: {data['message']}\n"
            
            return [TextContent(type="text", text=result)]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
        return [TextContent(type="text", text=error_msg)]
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        return [TextContent(type="text", text=error_msg)]


async def main():
    """Run the MCP server."""
    logger.info("Starting Futurama Quotes MCP Server...")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
