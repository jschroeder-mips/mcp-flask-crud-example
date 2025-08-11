"""
🤖 MCP Server for Flask Books API Integration
============================================

This MCP (Model Context Protocol) server provides tools for AI assistants
to interact with our Flask Books API. It's like a bridge between AI and our API!

Perfect for learning how to build MCP servers and integrate with REST APIs.

Author: GitHub Copilot 🤖  
Date: 2025-01-11
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import httpx
from mcp import ClientSession, StdioServerSession
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    ListToolsRequest,
    Tool,
    TextContent,
    ToolResult
)
from pydantic import BaseModel, ValidationError

# Configure logging 📊
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BookData(BaseModel):
    """
    📚 Pydantic model for book data validation.
    
    This ensures that our book data is properly structured and validated
    before sending it to the API. Type safety is important! 🛡️
    """
    title: str
    author: str
    year: int
    isbn: Optional[str] = None


class MCPBooksServer:
    """
    🤖 MCP Server for Books API Integration.
    
    This class implements an MCP server that provides tools for AI assistants
    to perform CRUD operations on our books API. Each tool corresponds to
    a different API endpoint!
    """
    
    def __init__(self, api_base_url: str = "http://localhost:5000") -> None:
        """
        Initialize the MCP Books Server.
        
        Args:
            api_base_url (str): Base URL of the Flask API server 🌐
        """
        self.api_base_url = api_base_url
        self.server = Server("books-mcp-server")
        self._setup_tools()
        
        # HTTP client for API requests 🌐
        self.http_client = httpx.AsyncClient(timeout=30.0)
        
        logger.info(f"🤖 MCP Books Server initialized with API at {api_base_url}")
    
    def _setup_tools(self) -> None:
        """
        🔧 Set up all the tools that the MCP server provides.
        
        Each tool represents a different operation that an AI assistant
        can perform with our books API.
        """
        
        # Tool 1: List all books 📚
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """Return the list of available tools."""
            return [
                Tool(
                    name="list_books",
                    description="📚 Get a list of all books in the collection. Returns book details including ID, title, author, year, and ISBN.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="get_book",
                    description="🔍 Get detailed information about a specific book by its ID.",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "book_id": {
                                "type": "integer",
                                "description": "The unique ID of the book to retrieve"
                            }
                        },
                        "required": ["book_id"]
                    }
                ),
                Tool(
                    name="create_book",
                    description="✨ Create a new book in the collection. Requires title, author, and publication year. ISBN is optional.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the book"
                            },
                            "author": {
                                "type": "string", 
                                "description": "The author of the book"
                            },
                            "year": {
                                "type": "integer",
                                "description": "The publication year"
                            },
                            "isbn": {
                                "type": "string",
                                "description": "Optional ISBN number"
                            }
                        },
                        "required": ["title", "author", "year"]
                    }
                ),
                Tool(
                    name="update_book",
                    description="✏️ Update an existing book's information. All fields except ID are optional.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "book_id": {
                                "type": "integer",
                                "description": "The ID of the book to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title for the book"
                            },
                            "author": {
                                "type": "string",
                                "description": "New author for the book"
                            },
                            "year": {
                                "type": "integer", 
                                "description": "New publication year"
                            },
                            "isbn": {
                                "type": "string",
                                "description": "New ISBN number"
                            }
                        },
                        "required": ["book_id"]
                    }
                ),
                Tool(
                    name="delete_book",
                    description="🗑️ Delete a book from the collection by its ID. This action cannot be undone!",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "book_id": {
                                "type": "integer",
                                "description": "The ID of the book to delete"
                            }
                        },
                        "required": ["book_id"]
                    }
                ),
                Tool(
                    name="health_check",
                    description="🏥 Check if the Books API is healthy and responding properly.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                )
            ]
        
        # Tool implementations 🛠️
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> ToolResult:
            """
            Handle tool calls from the MCP client.
            
            Args:
                name (str): Name of the tool to call
                arguments (Dict): Arguments for the tool
                
            Returns:
                ToolResult: Result of the tool execution
            """
            try:
                if name == "list_books":
                    return await self._list_books()
                elif name == "get_book":
                    return await self._get_book(arguments["book_id"])
                elif name == "create_book":
                    return await self._create_book(arguments)
                elif name == "update_book":
                    return await self._update_book(arguments)
                elif name == "delete_book":
                    return await self._delete_book(arguments["book_id"])
                elif name == "health_check":
                    return await self._health_check()
                else:
                    return ToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"❌ Unknown tool: {name}"
                        )],
                        isError=True
                    )
            
            except Exception as e:
                logger.error(f"Error in tool {name}: {str(e)}")
                return ToolResult(
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
    
    async def _list_books(self) -> ToolResult:
        """
        📚 Tool implementation: List all books.
        
        Returns:
            ToolResult: List of all books with formatting
        """
        try:
            data = await self._make_request("GET", "/books")
            books = data.get("books", [])
            count = data.get("count", 0)
            
            if not books:
                result_text = "📚 No books found in the collection!"
            else:
                result_text = f"📚 Found {count} books:\n\n"
                for book in books:
                    result_text += f"🆔 ID: {book['id']}\n"
                    result_text += f"📖 Title: {book['title']}\n"
                    result_text += f"✍️ Author: {book['author']}\n"
                    result_text += f"📅 Year: {book['year']}\n"
                    if book.get('isbn'):
                        result_text += f"🏷️ ISBN: {book['isbn']}\n"
                    result_text += f"⏰ Created: {book['created_at']}\n"
                    result_text += "─" * 40 + "\n\n"
            
            return ToolResult(
                content=[TextContent(type="text", text=result_text)]
            )
        
        except Exception as e:
            logger.error(f"Error listing books: {str(e)}")
            return ToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Failed to retrieve books: {str(e)}"
                )],
                isError=True
            )
    
    async def _get_book(self, book_id: int) -> ToolResult:
        """
        🔍 Tool implementation: Get a specific book.
        
        Args:
            book_id (int): ID of the book to retrieve
            
        Returns:
            ToolResult: Book details or error message
        """
        try:
            data = await self._make_request("GET", f"/books/{book_id}")
            book = data.get("book", {})
            
            result_text = f"📖 Book Details:\n\n"
            result_text += f"🆔 ID: {book['id']}\n"
            result_text += f"📚 Title: {book['title']}\n"
            result_text += f"✍️ Author: {book['author']}\n"
            result_text += f"📅 Year: {book['year']}\n"
            if book.get('isbn'):
                result_text += f"🏷️ ISBN: {book['isbn']}\n"
            result_text += f"⏰ Created: {book['created_at']}\n"
            result_text += f"🔄 Updated: {book['updated_at']}\n"
            
            return ToolResult(
                content=[TextContent(type="text", text=result_text)]
            )
        
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return ToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"❌ Book with ID {book_id} not found!"
                    )],
                    isError=True
                )
            raise
        
        except Exception as e:
            logger.error(f"Error getting book {book_id}: {str(e)}")
            return ToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Failed to retrieve book: {str(e)}"
                )],
                isError=True
            )
    
    async def _create_book(self, arguments: Dict[str, Any]) -> ToolResult:
        """
        ✨ Tool implementation: Create a new book.
        
        Args:
            arguments (Dict): Book creation data
            
        Returns:
            ToolResult: Created book details or error message
        """
        try:
            # Validate input data using Pydantic 🛡️
            book_data = BookData(**arguments)
            
            # Create the book via API
            data = await self._make_request("POST", "/books", book_data.dict())
            book = data.get("book", {})
            
            result_text = f"✨ Successfully created new book!\n\n"
            result_text += f"🆔 ID: {book['id']}\n"
            result_text += f"📚 Title: {book['title']}\n"
            result_text += f"✍️ Author: {book['author']}\n"
            result_text += f"📅 Year: {book['year']}\n"
            if book.get('isbn'):
                result_text += f"🏷️ ISBN: {book['isbn']}\n"
            result_text += f"⏰ Created: {book['created_at']}\n"
            
            return ToolResult(
                content=[TextContent(type="text", text=result_text)]
            )
        
        except ValidationError as e:
            return ToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Invalid book data: {str(e)}"
                )],
                isError=True
            )
        
        except Exception as e:
            logger.error(f"Error creating book: {str(e)}")
            return ToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Failed to create book: {str(e)}"
                )],
                isError=True
            )
    
    async def _update_book(self, arguments: Dict[str, Any]) -> ToolResult:
        """
        ✏️ Tool implementation: Update an existing book.
        
        Args:
            arguments (Dict): Update data including book_id
            
        Returns:
            ToolResult: Updated book details or error message
        """
        try:
            book_id = arguments.pop("book_id")
            
            # Filter out None values for partial updates
            update_data = {k: v for k, v in arguments.items() if v is not None}
            
            if not update_data:
                return ToolResult(
                    content=[TextContent(
                        type="text",
                        text="❌ No update data provided!"
                    )],
                    isError=True
                )
            
            # Update the book via API
            data = await self._make_request("PUT", f"/books/{book_id}", update_data)
            book = data.get("book", {})
            
            result_text = f"✏️ Successfully updated book!\n\n"
            result_text += f"🆔 ID: {book['id']}\n"
            result_text += f"📚 Title: {book['title']}\n"
            result_text += f"✍️ Author: {book['author']}\n"
            result_text += f"📅 Year: {book['year']}\n"
            if book.get('isbn'):
                result_text += f"🏷️ ISBN: {book['isbn']}\n"
            result_text += f"🔄 Updated: {book['updated_at']}\n"
            
            return ToolResult(
                content=[TextContent(type="text", text=result_text)]
            )
        
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return ToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"❌ Book with ID {arguments.get('book_id')} not found!"
                    )],
                    isError=True
                )
            raise
        
        except Exception as e:
            logger.error(f"Error updating book: {str(e)}")
            return ToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Failed to update book: {str(e)}"
                )],
                isError=True
            )
    
    async def _delete_book(self, book_id: int) -> ToolResult:
        """
        🗑️ Tool implementation: Delete a book.
        
        Args:
            book_id (int): ID of the book to delete
            
        Returns:
            ToolResult: Deletion confirmation or error message
        """
        try:
            await self._make_request("DELETE", f"/books/{book_id}")
            
            result_text = f"🗑️ Successfully deleted book with ID {book_id}!"
            
            return ToolResult(
                content=[TextContent(type="text", text=result_text)]
            )
        
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return ToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"❌ Book with ID {book_id} not found!"
                    )],
                    isError=True
                )
            raise
        
        except Exception as e:
            logger.error(f"Error deleting book {book_id}: {str(e)}")
            return ToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Failed to delete book: {str(e)}"
                )],
                isError=True
            )
    
    async def _health_check(self) -> ToolResult:
        """
        🏥 Tool implementation: Check API health.
        
        Returns:
            ToolResult: Health status of the API
        """
        try:
            data = await self._make_request("GET", "/health")
            
            result_text = f"🏥 API Health Check:\n\n"
            result_text += f"✅ Status: {data.get('status', 'Unknown')}\n"
            result_text += f"⏰ Timestamp: {data.get('timestamp', 'Unknown')}\n"
            result_text += f"💬 Message: {data.get('message', 'No message')}\n"
            
            return ToolResult(
                content=[TextContent(type="text", text=result_text)]
            )
        
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return ToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ API Health Check Failed: {str(e)}\n\nThe Flask API might not be running!"
                )],
                isError=True
            )
    
    async def run(self) -> None:
        """
        🚀 Run the MCP server using stdio transport.
        
        This method starts the server and keeps it running to handle
        MCP requests from clients.
        """
        try:
            logger.info("🤖 Starting MCP Books Server...")
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
    
    Creates and runs the MCP Books Server instance.
    """
    # You can customize the API URL here if your Flask app runs elsewhere
    api_url = "http://localhost:5000"
    
    server = MCPBooksServer(api_base_url=api_url)
    await server.run()


if __name__ == "__main__":
    """
    🚀 Run the MCP server when this file is executed directly.
    
    Usage:
    python mcp_server/server.py
    """
    print("🤖 Starting MCP Books Server...")
    print("📚 Connecting to Flask API at: http://localhost:5000")
    print("💡 Make sure your Flask API is running first!")
    print("🔌 This server provides tools for AI assistants to manage books")
    
    asyncio.run(main())