# � Futurama Quotes CRUD API + MCP Server + Frontend

Welcome to the year 3000! This comprehensive example demonstrates a Flask REST API for managing Futurama quotes with full CRUD operations, an MCP (Model Context Protocol) server for AI integration, and a simple themed frontend! Perfect for learning REST API development, AI tool integration, and web development. Good news everyone! 🤖

## 🎯 What You'll Learn

- **Flask REST API Development** - Build a complete CRUD API with proper error handling and Futurama theming
- **MCP Server Implementation** - Create tools for AI assistants to interact with your API from the year 3000
- **Frontend Development** - Simple but styled HTML/CSS/JavaScript interface
- **API Design Best Practices** - Proper HTTP status codes, JSON responses, and comprehensive documentation
- **Python Best Practices** - PEP8 compliance, type hints, and professional development standards
- **UV Package Management** - Modern Python package management instead of pip
- **Testing Strategies** - Comprehensive unit tests for both API and MCP server components

## 🏗️ Project Structure

```
📁 mcp-flask-crud-example/
├── 📋 README.md                   # You are here! 👋
├── ⚙️ pyproject.toml              # UV project configuration
├── 🚀 futurama_api/
│   ├── 📄 __init__.py
│   └── 🎯 app.py                  # Main Flask CRUD API for Futurama quotes
├── 🤖 mcp_server/
│   ├── 📄 __init__.py
│   └── 🛠️ server.py              # MCP server implementation
├── 🧪 tests/
│   └── 🌐 tests_test_api.py      # Comprehensive API tests
└── 📚 examples/
    ├── 🌐 api_examples.py         # API usage examples
    └── 🤖 mcp_examples.py         # MCP usage examples
```

## 🚀 Quick Start

### 1. Clone and Setup with UV

```bash
# Clone the repository
git clone https://github.com/jschroeder-mips/mcp-flask-crud-example.git
cd mcp-flask-crud-example

# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and create virtual environment
uv sync
```

### 2. Run the Flask API 🌐

```bash
# Activate the virtual environment and start the Flask API
uv run python futurama_api/app.py

# Or use the project script
uv run futurama-api

# The API will be available at:
# Frontend: http://localhost:5000/
# API: http://localhost:5000/api/quotes
```

### 3. Test the API 🧪

```bash
# In a new terminal, test the API
curl http://localhost:5000/health
curl http://localhost:5000/api/quotes

# Or open the frontend in your browser:
# http://localhost:5000/
```

### 4. Run the MCP Server 🤖

```bash
# In another terminal (keep Flask running!)
uv run python mcp_server/server.py

# Or use the project script
uv run futurama-mcp
```

## � API Endpoints

Our Futurama Quotes API provides these endpoints:

| Method | Endpoint | Description | Example |
|--------|----------|-------------|---------|
| `GET` | `/` | 🎨 Frontend interface | Open in browser |
| `GET` | `/health` | 🏥 Health check | `curl http://localhost:5000/health` |
| `GET` | `/api/quotes` | � List all quotes | `curl http://localhost:5000/api/quotes` |
| `GET` | `/api/quotes/{id}` | 🔍 Get specific quote | `curl http://localhost:5000/api/quotes/1` |
| `POST` | `/api/quotes` | ✨ Create new quote | `curl -X POST -H "Content-Type: application/json" -d '{"text":"Bite my shiny metal ass!","character":"Bender","episode":"Test"}' http://localhost:5000/api/quotes` |
| `PUT` | `/api/quotes/{id}` | ✏️ Update quote | `curl -X PUT -H "Content-Type: application/json" -d '{"text":"Updated quote"}' http://localhost:5000/api/quotes/1` |
| `DELETE` | `/api/quotes/{id}` | 🗑️ Delete quote | `curl -X DELETE http://localhost:5000/api/quotes/1` |

## 🎨 Frontend Features

The included frontend provides:

- **Futurama-themed styling** - Dark space theme with green terminal colors
- **Full CRUD operations** - Add, edit, update, and delete quotes
- **Real-time updates** - Automatically refreshes the quote list
- **Responsive design** - Works on desktop and mobile
- **Input validation** - Client-side form validation
- **Status messages** - User feedback for all operations

## 🤖 MCP Server Tools

The MCP server provides these tools for AI assistants:

- **`list_quotes`** � - Get all Futurama quotes in the collection
- **`get_quote`** 🔍 - Get details of a specific quote
- **`create_quote`** ✨ - Add a new quote to the collection
- **`update_quote`** ✏️ - Update an existing quote's information
- **`delete_quote`** 🗑️ - Remove a quote from the collection
- **`health_check`** 🏥 - Check if the API is healthy

## 💡 Understanding MCP (Model Context Protocol)

MCP is a protocol that allows AI assistants to interact with external services through **tools**. Think of it as a way for AI to call functions in your application from the year 3000!

### 🔄 How it Works:

1. **AI Assistant** wants to get Futurama quote information
2. **MCP Server** receives the request and validates parameters
3. **MCP Server** makes HTTP request to Flask API
4. **Flask API** processes the request and returns data
5. **MCP Server** formats the response for the AI
6. **AI Assistant** receives structured data to work with

### 🎯 Benefits:

- **Structured Communication** - Defined interfaces between AI and services
- **Type Safety** - Parameter validation and error handling with Pydantic
- **Better Integration** - AI can interact with any service through MCP
- **Standardization** - Consistent way to expose functionality to AI

## 📖 Code Examples

### 🌐 Using the Flask API

```python
import requests

# Get all quotes
response = requests.get('http://localhost:5000/api/quotes')
quotes = response.json()
print(f"Found {quotes['count']} quotes from the year 3000! �")

# Create a new quote
new_quote = {
    "text": "I'm back, baby!",
    "character": "Bender", 
    "episode": "Rebirth",
    "season": 6,
    "year": 2010
}

response = requests.post('http://localhost:5000/api/quotes', json=new_quote)
created_quote = response.json()
print(f"Created: {created_quote['quote']['text']} by {created_quote['quote']['character']} ✨")
```

### 🤖 Understanding MCP Tools

```python
# This is what an MCP tool looks like:
Tool(
    name="create_quote",
    description="✨ Create a new Futurama quote in the collection",
    inputSchema={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "The quote text"},
            "character": {"type": "string", "description": "Character who said it"},
            "episode": {"type": "string", "description": "Episode name"}
        },
        "required": ["text", "character", "episode"]
    }
)
```

## 🧪 Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=futurama_api --cov=mcp_server

# Run only API tests
uv run pytest tests/tests_test_api.py -v

# Run in watch mode during development
uv run pytest tests/ --watch
```

## 🛠️ Development

### Code Quality Tools

The project includes modern Python development tools:

```bash
# Format code with Black
uv run black futurama_api/ mcp_server/ tests/

# Lint with Ruff
uv run ruff check futurama_api/ mcp_server/ tests/

# Type checking with MyPy
uv run mypy futurama_api/ mcp_server/

# Install pre-commit hooks
uv run pre-commit install
```

### Adding Dependencies

```bash
# Add a new dependency
uv add requests

# Add a development dependency
uv add --dev pytest-cov

# Remove a dependency
uv remove requests
```

## 🐛 Common Issues & Solutions

1. **Port Already in Use** 🚫
   ```bash
   # Find process using port 5000
   lsof -i :5000
   # Kill the process
   kill -9 <PID>
   ```

2. **MCP Server Can't Connect** 🔌
   - Make sure Flask API is running first
   - Check the API URL in `mcp_server/server.py`
   - Verify port 5000 is accessible

3. **Import Errors** 📦
   - Ensure UV virtual environment is activated: `uv shell`
   - Reinstall dependencies: `uv sync`

## ✨ Sample Quotes Included

The API comes pre-loaded with classic Futurama quotes:

- "Bite my shiny metal ass!" - Bender
- "Good news everyone!" - Professor Farnsworth  
- "Shut up and take my money!" - Fry
- "Why not Zoidberg?" - Dr. Zoidberg
- "I'm going to build my own theme park, with blackjack and hookers!" - Bender

## 📚 Learning Resources

- **Flask Documentation** - https://flask.palletsprojects.com/
- **MCP Specification** - https://spec.modelcontextprotocol.io/
- **UV Documentation** - https://docs.astral.sh/uv/
- **REST API Best Practices** - https://restfulapi.net/
- **Python Type Hints** - https://docs.python.org/3/library/typing.html
- **Pydantic Validation** - https://docs.pydantic.dev/

## 🤝 Contributing

Found a bug? Want to add features? Contributions welcome! 

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `uv run pytest`
5. Format code: `uv run black .`
6. Submit a pull request! 🚀

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 Acknowledgments

- Built with ❤️ for learning and teaching
- Inspired by the amazing show Futurama
- Perfect for developers learning modern Python development! 🌟
- Uses UV for fast, reliable dependency management
- Demonstrates professional Python project structure

---

**Good news everyone! Happy Coding from the year 3000!** 🚀�🤖

If you have questions or need help, feel free to open an issue or reach out!

*"Bite my shiny metal API!"* - Bender 🤖