"""
🤖 MCP Server for Futurama Quotes API Integration
=================================================

This MCP (Model Context Protocol) server provides tools for AI assistants
to interact with our Futurama Quotes API. It's like a bridge between AI and the year 3000!

Perfect for learning how to build MCP servers and integrate with REST APIs.
Good news everyone! This server makes it easy to manage Futurama quotes with AI!

Author: GitHub Copilot 🤖  
Date: 2025-01-11
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import httpx
from mcp import ClientSession, ServerSession
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    ListToolsRequest,
    Tool,
    TextContent,
    CallToolResult
)
from pydantic import BaseModel, ValidationError

# Configure logging 📊
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuoteData(BaseModel):
    """
    � Pydantic model for Futurama quote data validation.
    
    This ensures that our quote data is properly structured and validated
    before sending it to the API. Type safety is important in the year 3000! 🛡️
    """
    text: str
    character: str
    episode: str
    season: Optional[int] = None
    year: Optional[int] = None


class MCPQuotesServer:
    """
    🤖 MCP Server for Futurama Quotes API Integration.
    
    This class implements an MCP server that provides tools for AI assistants
    to perform CRUD operations on our Futurama quotes API. Each tool corresponds to
    a different API endpoint! Good news everyone!
    """
    
    def __init__(self, api_base_url: str = "http://localhost:5000") -> None:
        """
        Initialize the MCP Quotes Server.
        
        Args:
            api_base_url (str): Base URL of the Flask API server 🌐
        """
        self.api_base_url = api_base_url
        self.server = Server("futurama-quotes-mcp-server")
        self._setup_tools()
        
        # HTTP client for API requests 🌐
        self.http_client = httpx.AsyncClient(timeout=30.0)
        
        logger.info(f"🤖 MCP Futurama Quotes Server initialized with API at {api_base_url}")
    
    def _setup_tools(self) -> None:
        """
        🔧 Set up all the tools that the MCP server provides.
        
        Each tool represents a different operation that an AI assistant
        can perform with our Futurama quotes API. Good news everyone!
        """
        
        # Tool 1: List all quotes �
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """Return the list of available tools."""
            return [
                Tool(
                    name="list_quotes",
                    description="� Get a list of all Futurama quotes in the collection. Returns quote details including ID, text, character, episode, season, and year.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="get_quote",
                    description="🔍 Get detailed information about a specific Futurama quote by its ID.",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "quote_id": {
                                "type": "integer",
                                "description": "The unique ID of the quote to retrieve"
                            }
                        },
                        "required": ["quote_id"]
                    }
                ),
                Tool(
                    name="create_quote",
                    description="✨ Create a new Futurama quote in the collection. Requires text, character, and episode. Season and year are optional.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "The text of the Futurama quote"
                            },
                            "character": {
                                "type": "string", 
                                "description": "The character who said the quote (e.g., Bender, Fry, Professor)"
                            },
                            "episode": {
                                "type": "string",
                                "description": "The episode name or identifier"
                            },
                            "season": {
                                "type": "integer",
                                "description": "Optional season number"
                            },
                            "year": {
                                "type": "integer",
                                "description": "Optional year the episode aired"
                            }
                        },
                        "required": ["text", "character", "episode"]
                    }
                ),
                Tool(
                    name="update_quote",
                    description="✏️ Update an existing Futurama quote's information. All fields except ID are optional.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "quote_id": {
                                "type": "integer",
                                "description": "The ID of the quote to update"
                            },
                            "text": {
                                "type": "string",
                                "description": "New text for the quote"
                            },
                            "character": {
                                "type": "string",
                                "description": "New character for the quote"
                            },
                            "episode": {
                                "type": "string", 
                                "description": "New episode for the quote"
                            },
                            "season": {
                                "type": "integer",
                                "description": "New season number"
                            },
                            "year": {
                                "type": "integer",
                                "description": "New year"
                            }
                        },
                        "required": ["quote_id"]
                    }
                ),
                Tool(
                    name="delete_quote",
                    description="🗑️ Delete a Futurama quote from the collection by its ID. This action cannot be undone!",
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
                    description="🏥 Check if the Futurama Quotes API is healthy and responding properly.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                )
            ]
        
        # Tool implementations 🛠️
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """
            Handle tool calls from the MCP client.
            
            Args:
                name (str): Name of the tool to call
                arguments (Dict): Arguments for the tool
                
            Returns:
                CallToolResult: Result of the tool execution
            """
            try:
                if name == "list_quotes":
                    return await self._list_quotes()
                elif name == "get_quote":
                    return await self._get_quote(arguments["quote_id"])
                elif name == "create_quote":
                    return await self._create_quote(arguments)
                elif name == "update_quote":
                    return await self._update_quote(arguments)
                elif name == "delete_quote":
                    return await self._delete_quote(arguments["quote_id"])
                elif name == "health_check":
                    return await self._health_check()
                else:
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"❌ Unknown tool: {name}"
                        )],
                        isError=True
                    )
            
            except Exception as e:
                logger.error(f"Error in tool {name}: {str(e)}")
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"❌ Error executing {name}: {str(e)}"
                    )],
                    isError=True
                )
    
    async def _make_request(self, method: str, endpoint: str, 
                          json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        🌐 Make an HTTP request to the Flask API.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint path
            json_data (Dict, optional): JSON data for POST/PUT requests
            
        Returns:
            Dict: Response data from the API
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        url = urljoin(self.api_base_url, endpoint)
        
        try:
            response = await self.http_client.request(
                method=method,
                url=url,
                json=json_data,
                headers={"Content-Type": "application/json"}
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            return response.json()
        
        except httpx.HTTPError as e:
            logger.error(f"HTTP request failed: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise
    
    async def _list_quotes(self) -> CallToolResult:
        """
        � Tool implementation: List all Futurama quotes.
        
        Returns:
            CallToolResult: List of all quotes with Futurama-themed formatting
        """
        try:
            data = await self._make_request("GET", "/quotes")
            quotes = data.get("quotes", [])
            count = data.get("count", 0)
            
            if not quotes:
                result_text = "� No quotes found from the year 3000!"
            else:
                result_text = f"� Found {count} quotes from Futurama:\n\n"
                for quote in quotes:
                    result_text += f"🆔 ID: {quote['id']}\n"
                    result_text += f"� Quote: \"{quote['text']}\"\n"
                    result_text += f"🎭 Character: {quote['character']}\n"
                    result_text += f"� Episode: {quote['episode']}\n"
                    if quote.get('season'):
                        result_text += f"📅 Season: {quote['season']}\n"
                    if quote.get('year'):
                        result_text += f"🗓️ Year: {quote['year']}\n"
                    result_text += f"⏰ Created: {quote['created_at']}\n"
                    result_text += "─" * 40 + "\n\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)]
            )
        
        except Exception as e:
            logger.error(f"Error listing quotes: {str(e)}")
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Failed to retrieve quotes from the year 3000: {str(e)}"
                )],
                isError=True
            )
    
    async def _get_quote(self, quote_id: int) -> CallToolResult:
        """
        🔍 Tool implementation: Get a specific Futurama quote.
        
        Args:
            quote_id (int): ID of the quote to retrieve
            
        Returns:
            CallToolResult: Quote details or error message
        """
        try:
            data = await self._make_request("GET", f"/quotes/{quote_id}")
            quote = data.get("quote", {})
            
            result_text = f"� Futurama Quote Details:\n\n"
            result_text += f"🆔 ID: {quote['id']}\n"
            result_text += f"� Quote: \"{quote['text']}\"\n"
            result_text += f"🎭 Character: {quote['character']}\n"
            result_text += f"📺 Episode: {quote['episode']}\n"
            if quote.get('season'):
                result_text += f"📅 Season: {quote['season']}\n"
            if quote.get('year'):
                result_text += f"🗓️ Year: {quote['year']}\n"
            result_text += f"⏰ Created: {quote['created_at']}\n"
            result_text += f"🔄 Updated: {quote['updated_at']}\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)]
            )
        
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"❌ Quote with ID {quote_id} not found in the year 3000!"
                    )],
                    isError=True
                )
            raise
        
        except Exception as e:
            logger.error(f"Error getting quote {quote_id}: {str(e)}")
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Failed to retrieve quote: {str(e)}"
                )],
                isError=True
            )
    
    async def _create_quote(self, arguments: Dict[str, Any]) -> CallToolResult:
        """
        ✨ Tool implementation: Create a new Futurama quote.
        
        Args:
            arguments (Dict): Quote creation data
            
        Returns:
            CallToolResult: Created quote details or error message
        """
        try:
            # Validate input data using Pydantic 🛡️
            quote_data = QuoteData(**arguments)
            
            # Create the quote via API
            data = await self._make_request("POST", "/quotes", quote_data.dict())
            quote = data.get("quote", {})
            
            result_text = f"✨ Successfully created new Futurama quote!\n\n"
            result_text += f"🆔 ID: {quote['id']}\n"
            result_text += f"� Quote: \"{quote['text']}\"\n"
            result_text += f"🎭 Character: {quote['character']}\n"
            result_text += f"📺 Episode: {quote['episode']}\n"
            if quote.get('season'):
                result_text += f"📅 Season: {quote['season']}\n"
            if quote.get('year'):
                result_text += f"🗓️ Year: {quote['year']}\n"
            result_text += f"⏰ Created: {quote['created_at']}\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)]
            )
        
        except ValidationError as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Invalid quote data: {str(e)}"
                )],
                isError=True
            )
        
        except Exception as e:
            logger.error(f"Error creating quote: {str(e)}")
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Failed to create quote: {str(e)}"
                )],
                isError=True
            )
    
    async def _update_quote(self, arguments: Dict[str, Any]) -> CallToolResult:
        """
        ✏️ Tool implementation: Update an existing Futurama quote.
        
        Args:
            arguments (Dict): Update data including quote_id
            
        Returns:
            CallToolResult: Updated quote details or error message
        """
        try:
            quote_id = arguments.pop("quote_id")
            
            # Filter out None values for partial updates
            update_data = {k: v for k, v in arguments.items() if v is not None}
            
            if not update_data:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text="❌ No update data provided, meatbag!"
                    )],
                    isError=True
                )
            
            # Update the quote via API
            data = await self._make_request("PUT", f"/quotes/{quote_id}", update_data)
            quote = data.get("quote", {})
            
            result_text = f"✏️ Successfully updated Futurama quote!\n\n"
            result_text += f"🆔 ID: {quote['id']}\n"
            result_text += f"� Quote: \"{quote['text']}\"\n"
            result_text += f"🎭 Character: {quote['character']}\n"
            result_text += f"📺 Episode: {quote['episode']}\n"
            if quote.get('season'):
                result_text += f"📅 Season: {quote['season']}\n"
            if quote.get('year'):
                result_text += f"🗓️ Year: {quote['year']}\n"
            result_text += f"🔄 Updated: {quote['updated_at']}\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)]
            )
        
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"❌ Quote with ID {arguments.get('quote_id')} not found in the year 3000!"
                    )],
                    isError=True
                )
            raise
        
        except Exception as e:
            logger.error(f"Error updating quote: {str(e)}")
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Failed to update quote: {str(e)}"
                )],
                isError=True
            )
    
    async def _delete_quote(self, quote_id: int) -> CallToolResult:
        """
        🗑️ Tool implementation: Delete a Futurama quote.
        
        Args:
            quote_id (int): ID of the quote to delete
            
        Returns:
            CallToolResult: Deletion confirmation or error message
        """
        try:
            await self._make_request("DELETE", f"/quotes/{quote_id}")
            
            result_text = f"🗑️ Successfully deleted Futurama quote with ID {quote_id}! Bite my shiny metal ass!"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)]
            )
        
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"❌ Quote with ID {quote_id} not found in the year 3000!"
                    )],
                    isError=True
                )
            raise
        
        except Exception as e:
            logger.error(f"Error deleting quote {quote_id}: {str(e)}")
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Failed to delete quote: {str(e)}"
                )],
                isError=True
            )
    
    async def _health_check(self) -> CallToolResult:
        """
        🏥 Tool implementation: Check API health.
        
        Returns:
            CallToolResult: Health status of the Futurama API
        """
        try:
            data = await self._make_request("GET", "/health")
            
            result_text = f"🏥 Futurama Quotes API Health Check:\n\n"
            result_text += f"✅ Status: {data.get('status', 'Unknown')}\n"
            result_text += f"⏰ Timestamp: {data.get('timestamp', 'Unknown')}\n"
            result_text += f"💬 Message: {data.get('message', 'No message from the year 3000')}\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)]
            )
        
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Futurama API Health Check Failed: {str(e)}\n\nThe Flask API might not be running in the year 3000!"
                )],
                isError=True
            )
    
    async def run(self) -> None:
        """
        🚀 Run the MCP server using stdio transport.
        
        This method starts the server and keeps it running to handle
        MCP requests from clients in the year 3000!
        """
        try:
            logger.info("🤖 Starting MCP Futurama Quotes Server...")
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
        except KeyboardInterrupt:
            logger.info("🛑 MCP Server stopped by user")
        except Exception as e:
            logger.error(f"❌ MCP Server error: {str(e)}")
        finally:
            await self.http_client.aclose()
            logger.info("🔚 MCP Server shutdown complete")


async def main() -> None:
    """
    🎯 Main entry point for the MCP server.
    
    Creates and runs the MCP Futurama Quotes Server instance.
    Good news everyone!
    """
    # You can customize the API URL here if your Flask app runs elsewhere
    api_url = "http://localhost:5000"
    
    server = MCPQuotesServer(api_base_url=api_url)
    await server.run()


if __name__ == "__main__":
    """
    🚀 Run the MCP server when this file is executed directly.
    
    Usage:
    python mcp_server/server.py
    """
    print("🤖 Starting MCP Futurama Quotes Server...")
    print("� Connecting to Flask API at: http://localhost:5000")
    print("💡 Make sure your Flask API is running first!")
    print("🔌 This server provides tools for AI assistants to manage Futurama quotes")
    print("🚀 Good news everyone! The MCP server is starting up!")
    
    asyncio.run(main())