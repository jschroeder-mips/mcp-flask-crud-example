# 📚 Flask CRUD + MCP Server Example

A comprehensive example demonstrating a Flask REST API with full CRUD operations and an MCP (Model Context Protocol) server for AI integration! Perfect for learning both REST API development and AI tool integration. 🚀

## 🎯 What You'll Learn

- **Flask REST API Development** - Build a complete CRUD API with proper error handling
- **MCP Server Implementation** - Create tools for AI assistants to interact with your API
- **API Design Best Practices** - Proper HTTP status codes, JSON responses, and documentation
- **Python Best Practices** - PEP8 compliance, type hints, and comprehensive documentation
- **Testing Strategies** - Unit tests for both API and MCP server components

## 🏗️ Project Structure

```
📁 mcp-flask-crud-example/
├── 📋 README.md                   # You are here! 👋
├── 📦 requirements.txt            # Python dependencies
├── 🚀 setup_and_run.py           # Easy setup script
├── 🌐 flask_api/
│   ├── 📄 __init__.py
│   └── 🎯 app.py                  # Main Flask CRUD API
├── 🤖 mcp_server/
│   ├── 📄 __init__.py
│   └── 🛠️ server.py              # MCP server implementation
├── 🧪 tests/
│   ├── 📄 __init__.py
│   ├── 🌐 test_api.py            # API tests
│   └── 🤖 test_mcp.py            # MCP server tests
└── 📚 examples/
    ├── 🌐 api_examples.py         # API usage examples
    └── 🤖 mcp_examples.py         # MCP usage examples
```

## 🚀 Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/jschroeder-mips/mcp-flask-crud-example.git
cd mcp-flask-crud-example

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Flask API 🌐
```bash
# Start the Flask API server
python flask_api/app.py

# The API will be available at:
# http://localhost:5000
```

### 3. Test the API 🧪
```bash
# In a new terminal, test the API
curl http://localhost:5000/health
curl http://localhost:5000/books
```

### 4. Run the MCP Server 🤖
```bash
# In another terminal (keep Flask running!)
python mcp_server/server.py
```

## 📚 API Endpoints

Our Books API provides these endpoints:

| Method | Endpoint | Description | Example |
|--------|----------|-------------|---------|
| `GET` | `/health` | 🏥 Health check | `curl http://localhost:5000/health` |
| `GET` | `/books` | 📚 List all books | `curl http://localhost:5000/books` |
| `GET` | `/books/{id}` | 🔍 Get specific book | `curl http://localhost:5000/books/1` |
| `POST` | `/books` | ✨ Create new book | `curl -X POST -H "Content-Type: application/json" -d '{"title":"New Book","author":"Author Name","year":2024}' http://localhost:5000/books` |
| `PUT` | `/books/{id}` | ✏️ Update book | `curl -X PUT -H "Content-Type: application/json" -d '{"title":"Updated Title"}' http://localhost:5000/books/1` |
| `DELETE` | `/books/{id}` | 🗑️ Delete book | `curl -X DELETE http://localhost:5000/books/1` |

## 🤖 MCP Server Tools

The MCP server provides these tools for AI assistants:

- **`list_books`** 📚 - Get all books in the collection
- **`get_book`** 🔍 - Get details of a specific book
- **`create_book`** ✨ - Add a new book to the collection
- **`update_book`** ✏️ - Update an existing book's information
- **`delete_book`** 🗑️ - Remove a book from the collection
- **`health_check`** 🏥 - Check if the API is healthy

## 💡 Understanding MCP (Model Context Protocol)

MCP is a protocol that allows AI assistants to interact with external services through **tools**. Think of it as a way for AI to call functions in your application!

### 🔄 How it Works:

1. **AI Assistant** wants to get book information
2. **MCP Server** receives the request and validates parameters
3. **MCP Server** makes HTTP request to Flask API
4. **Flask API** processes the request and returns data
5. **MCP Server** formats the response for the AI
6. **AI Assistant** receives structured data to work with

### 🎯 Benefits:

- **Structured Communication** - Defined interfaces between AI and services
- **Type Safety** - Parameter validation and error handling
- **Better Integration** - AI can interact with any service through MCP
- **Standardization** - Consistent way to expose functionality to AI

## 📖 Code Examples

### 🌐 Using the Flask API

```python
import requests

# Get all books
response = requests.get('http://localhost:5000/books')
books = response.json()
print(f"Found {books['count']} books! 📚")

# Create a new book
new_book = {
    "title": "Python Tricks",
    "author": "Dan Bader", 
    "year": 2017,
    "isbn": "978-1775093305"
}

response = requests.post('http://localhost:5000/books', json=new_book)
created_book = response.json()
print(f"Created: {created_book['book']['title']} ✨")
```

### 🤖 Understanding MCP Tools

```python
# This is what an MCP tool looks like:
Tool(
    name="create_book",
    description="✨ Create a new book in the collection",
    inputSchema={
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Book title"},
            "author": {"type": "string", "description": "Book author"},
            "year": {"type": "integer", "description": "Publication year"}
        },
        "required": ["title", "author", "year"]
    }
)
```

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run only API tests
python -m pytest tests/test_api.py -v

# Run only MCP tests  
python -m pytest tests/test_mcp.py -v

# Run tests with coverage
python -m pytest tests/ --cov=flask_api --cov=mcp_server
```

## 🛠️ Development Tips

### 🐛 Common Issues & Solutions

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
   - Activate your virtual environment
   - Install dependencies: `pip install -r requirements.txt`

### ✨ Extending the Code

**Add New Fields to Books:**
```python
# In flask_api/app.py, update the Book class:
class Book:
    def __init__(self, book_id, title, author, year, isbn=None, genre=None):
        # ... existing code ...
        self.genre = genre
```

**Add New MCP Tools:**
```python
# In mcp_server/server.py, add to list_tools():
Tool(
    name="search_books",
    description="🔍 Search books by title or author",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"}
        },
        "required": ["query"]
    }
)
```

## 📚 Learning Resources

- **Flask Documentation** - https://flask.palletsprojects.com/
- **MCP Specification** - https://spec.modelcontextprotocol.io/
- **REST API Best Practices** - https://restfulapi.net/
- **Python Type Hints** - https://docs.python.org/3/library/typing.html
- **Pydantic Validation** - https://pydantic-docs.helpmanual.io/

## 🤝 Contributing

Found a bug? Want to add features? Contributions welcome! 

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `python -m pytest`
5. Submit a pull request! 🚀

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Acknowledgments

- Built with ❤️ for learning and teaching
- Inspired by the need for practical MCP examples
- Perfect for junior developers starting their journey! 🌟

---

**Happy Coding!** 🚀📚🤖

If you have questions or need help, feel free to open an issue or reach out!