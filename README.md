# Futurama Quotes API with MCP Server

A complete CRUD application featuring a Flask REST API for managing Futurama quotes and an MCP (Model Context Protocol) server that provides AI-friendly access to the API.

**🎯 Ready to use!** Includes 263+ Futurama quotes that load automatically - no setup required!

## 🚀 Features

- **RESTful Flask API** with full CRUD operations
- **MCP Server** for AI assistant integration
- **Auto-loading quotes** from JSON file at startup (263+ Futurama quotes included!)
- **CORS enabled** for frontend integration
- **Comprehensive error handling** and logging
- **Docker-ready** setup scripts

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [MCP Server Documentation](#mcp-server-documentation)
- [Installation & Setup](#installation--setup)
- [Usage Examples](#usage-examples)
- [Development](#development)
- [Contributing](#contributing)

## 🚀 Quick Start

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd mcp-flask-crud-example
   ./setup.sh
   ```

2. **Start the Flask API:**
   ```bash
   python futurama_api/app.py
   ```
   The API automatically loads 263+ Futurama quotes from the included JSON file.

3. **Start the MCP Server (in another terminal):**
   ```bash
   ./run_mcp_server.sh
   ```

4. **Test the API:**
   ```bash
   curl http://localhost:5000/health
   curl http://localhost:5000/api/quotes
   ```

##  Project Structure

```
mcp-flask-crud-example/
├── futurama_api/           # Flask REST API
│   ├── __init__.py
│   ├── app.py             # Main Flask application
│   └── futurama_quotes.json # 263+ Futurama quotes (auto-loaded)
├── mcp_server/            # MCP Server for AI integration
│   ├── __init__.py
│   └── server.py          # MCP server implementation
├── requirements.txt       # Python dependencies
├── setup.sh              # Automated setup script
├── run_mcp_server.sh     # MCP server launcher
└── README.md             # This file
```

## 🔧 API Documentation

### Base URL
```
http://localhost:5000
```

### Health Check
```http
GET /health
```

**Response:**
```json
{
    "status": "healthy",
    "message": "Futurama Quotes API is running"
}
```

### Quotes Endpoints

#### Get All Quotes
```http
GET /api/quotes
```

**Response:**
```json
{
    "count": 4,
    "quotes": [
        {
            "id": 1,
            "text": "Bite my shiny metal ass!",
            "character": "Bender",
            "episode": "A Fishful of Dollars",
            "created_at": "2025-08-13T10:30:00"
        }
    ]
}
```

#### Get Quote by ID
```http
GET /api/quotes/{id}
```

**Response:**
```json
{
    "id": 1,
    "text": "Bite my shiny metal ass!",
    "character": "Bender",
    "episode": "A Fishful of Dollars",
    "created_at": "2025-08-13T10:30:00"
}
```

#### Create New Quote
```http
POST /api/quotes
Content-Type: application/json

{
    "text": "I'm gonna build my own theme park!",
    "character": "Bender",
    "episode": "Godfellas"
}
```

**Response:**
```json
{
    "id": 5,
    "text": "I'm gonna build my own theme park!",
    "character": "Bender",
    "episode": "Godfellas",
    "created_at": "2025-08-13T11:45:00"
}
```

#### Update Quote
```http
PUT /api/quotes/{id}
Content-Type: application/json

{
    "text": "Updated quote text",
    "character": "Updated character"
}
```

#### Delete Quote
```http
DELETE /api/quotes/{id}
```

**Response:**
```json
{
    "message": "Quote deleted successfully"
}
```

## 🤖 MCP Server Documentation

The MCP server provides AI assistants with structured access to the Futurama Quotes API through the Model Context Protocol.

### Available MCP Tools

#### `list_quotes`
- **Description:** Get all Futurama quotes
- **Parameters:** None
- **Returns:** Formatted list of all quotes

#### `get_quote`
- **Description:** Get a specific quote by ID
- **Parameters:** 
  - `quote_id` (integer, required): The ID of the quote
- **Returns:** Detailed quote information

#### `create_quote`
- **Description:** Create a new quote
- **Parameters:**
  - `text` (string, required): Quote text
  - `character` (string, required): Character name
  - `episode` (string, required): Episode name
  - `season` (integer, optional): Season number
  - `year` (integer, optional): Year
- **Returns:** Created quote details

#### `update_quote`
- **Description:** Update an existing quote
- **Parameters:**
  - `quote_id` (integer, required): The ID of the quote to update
  - `text` (string, optional): Updated quote text
  - `character` (string, optional): Updated character name
  - `episode` (string, optional): Updated episode name
  - `season` (integer, optional): Updated season number
  - `year` (integer, optional): Updated year
- **Returns:** Updated quote details

#### `delete_quote`
- **Description:** Delete a quote by ID
- **Parameters:**
  - `quote_id` (integer, required): The ID of the quote to delete
- **Returns:** Deletion confirmation

#### `health_check`
- **Description:** Check API health status
- **Parameters:** None
- **Returns:** API health status

### Installing on Claude Desktop

To use this MCP server with Claude Desktop, follow these steps:

#### 1. Complete Project Setup
First, ensure the project is properly set up:
```bash
git clone <repository-url>
cd mcp-flask-crud-example
./setup.sh
```

#### 2. Find Your Configuration File
Claude Desktop stores MCP server configurations in a JSON file. The location depends on your operating system:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

#### 3. Configure the MCP Server
Add the following configuration to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "futurama-quotes": {
      "command": "/absolute/path/to/mcp-flask-crud-example/run_mcp_server.sh",
      "args": [],
      "env": {}
    }
  }
}
```

**Important:** Replace `/absolute/path/to/mcp-flask-crud-example/` with the actual absolute path to your project directory.

#### 4. Make the Script Executable
Ensure the run script has execute permissions:
```bash
chmod +x run_mcp_server.sh
```

#### 5. Start the Flask API
Before using the MCP server, make sure the Flask API is running:
```bash
python futurama_api/app.py
```
Keep this running in a separate terminal window.

#### 6. Restart Claude Desktop
After adding the configuration, restart Claude Desktop for the changes to take effect.

#### 7. Verify Integration
In Claude Desktop, you should now be able to:
- Ask "What Futurama quotes do you have?"
- Say "Create a new quote by Bender"
- Request "Show me quote number 2"
- Ask "Delete quote 3"

The MCP server will automatically handle the communication between Claude and your Flask API.

#### Troubleshooting Claude Desktop Integration

**If Claude can't connect to the MCP server:**
1. Check that the path in `claude_desktop_config.json` is absolute and correct
2. Ensure the Flask API is running on `localhost:5000`
3. Verify the `run_mcp_server.sh` script has execute permissions
4. Check Claude Desktop's logs for error messages
5. Test the MCP server manually: `./run_mcp_server.sh`

**Configuration Example with Full Path on MacOS:**
```json
{
  "mcpServers": {
    "futurama-quotes": {
      "command": "/Users/jschroeder/Documents/code_repos/mcp-flask-crud-example/run_mcp_server.sh",
      "args": [],
      "env": {}
    }
  }
}
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Automated Setup
```bash
./setup.sh
```

This script will:
- Create a Python virtual environment
- Install all dependencies
- Set up the project structure
- Provide usage instructions

### Manual Setup
1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python -c "import flask, mcp, httpx; print('All dependencies installed!')"
   ```

## 💡 Usage Examples

### Using the REST API directly

```bash
# Get all quotes
curl http://localhost:5000/api/quotes

# Get specific quote
curl http://localhost:5000/api/quotes/1

# Create new quote
curl -X POST http://localhost:5000/api/quotes \
  -H "Content-Type: application/json" \
  -d '{"text":"New quote","character":"Fry","episode":"Test Episode"}'

# Update quote
curl -X PUT http://localhost:5000/api/quotes/1 \
  -H "Content-Type: application/json" \
  -d '{"text":"Updated quote text"}'

# Delete quote
curl -X DELETE http://localhost:5000/api/quotes/1
```

### Using with AI Assistants

Once the MCP server is running, AI assistants can use natural language to interact with your quotes:

- "Show me all Futurama quotes"
- "Create a new quote by Bender"
- "Update quote 3 to have different text"
- "Delete quote 2"

## 🔧 Development

### Running in Development Mode

1. **Start Flask API (with auto-reload):**
   ```bash
   cd futurama_api
   python app.py
   ```

2. **Start MCP Server:**
   ```bash
   ./run_mcp_server.sh
   ```

### Project Dependencies

- **Flask 3.0+**: Web framework for the REST API
- **Flask-CORS 4.0+**: Cross-origin resource sharing support
- **MCP 1.0+**: Model Context Protocol server implementation
- **httpx 0.27+**: Async HTTP client for MCP server

### Adding New Features

1. **Add API endpoints** in `futurama_api/app.py`
2. **Add corresponding MCP tools** in `mcp_server/server.py`
3. **Update documentation** in this README
4. **Test thoroughly** with both REST and MCP interfaces

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Futurama** for the hilarious quotes
- **Flask** team for the excellent web framework
- **MCP Protocol** for enabling AI integration
- **GitHub Copilot** for development assistance

---

*"Good news everyone! Your quotes are now AI-accessible!"* - Professor Farnsworth
