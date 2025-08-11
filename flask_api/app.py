"""
🚀 Flask CRUD REST API for Books Management
===========================================

This module provides a simple REST API for managing books with full CRUD operations.
Perfect for learning REST API development and MCP server integration!

Author: GitHub Copilot 🤖
Date: 2025-01-11
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, List, Optional, Union
import logging
from datetime import datetime

# Configure logging for better debugging 📊
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Book:
    """
    📚 Book model class for our simple book management system.
    
    This class represents a book with basic properties like title, author, etc.
    It's designed to be simple and easy to understand for junior developers!
    """
    
    def __init__(self, book_id: int, title: str, author: str, 
                 year: int, isbn: Optional[str] = None) -> None:
        """
        Initialize a new Book instance.
        
        Args:
            book_id (int): Unique identifier for the book 🆔
            title (str): The title of the book 📖
            author (str): The author's name ✍️
            year (int): Publication year 📅
            isbn (str, optional): ISBN number if available
        """
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Union[str, int]]:
        """
        Convert the Book instance to a dictionary for JSON serialization.
        
        Returns:
            Dict: Dictionary representation of the book 📋
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'isbn': self.isbn,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def update(self, title: Optional[str] = None, author: Optional[str] = None, 
               year: Optional[int] = None, isbn: Optional[str] = None) -> None:
        """
        Update book properties and timestamp.
        
        Args:
            title (str, optional): New title
            author (str, optional): New author
            year (int, optional): New year
            isbn (str, optional): New ISBN
        """
        if title is not None:
            self.title = title
        if author is not None:
            self.author = author
        if year is not None:
            self.year = year
        if isbn is not None:
            self.isbn = isbn
        self.updated_at = datetime.now().isoformat()


class BookManager:
    """
    📚 Simple in-memory book storage manager.
    
    This class handles all CRUD operations for books. In a real application,
    you'd replace this with a proper database like PostgreSQL or MongoDB!
    """
    
    def __init__(self) -> None:
        """Initialize the book manager with some sample data."""
        self.books: Dict[int, Book] = {}
        self.next_id = 1
        self._initialize_sample_data()
    
    def _initialize_sample_data(self) -> None:
        """Add some sample books to get started! 📚✨"""
        sample_books = [
            Book(1, "The Python Cookbook", "David Beazley", 2013, "978-1449340377"),
            Book(2, "Flask Web Development", "Miguel Grinberg", 2018, "978-1491991732"),
            Book(3, "Clean Code", "Robert C. Martin", 2008, "978-0132350884")
        ]
        
        for book in sample_books:
            self.books[book.id] = book
            self.next_id = max(self.next_id, book.id + 1)
    
    def get_all_books(self) -> List[Dict[str, Union[str, int]]]:
        """
        Get all books in the collection.
        
        Returns:
            List[Dict]: List of all books as dictionaries 📚
        """
        return [book.to_dict() for book in self.books.values()]
    
    def get_book(self, book_id: int) -> Optional[Dict[str, Union[str, int]]]:
        """
        Get a specific book by ID.
        
        Args:
            book_id (int): The ID of the book to retrieve
            
        Returns:
            Dict or None: Book dictionary if found, None otherwise 🔍
        """
        book = self.books.get(book_id)
        return book.to_dict() if book else None
    
    def create_book(self, title: str, author: str, year: int, 
                   isbn: Optional[str] = None) -> Dict[str, Union[str, int]]:
        """
        Create a new book.
        
        Args:
            title (str): Book title
            author (str): Book author
            year (int): Publication year
            isbn (str, optional): ISBN number
            
        Returns:
            Dict: The newly created book as a dictionary ✨
        """
        new_book = Book(self.next_id, title, author, year, isbn)
        self.books[self.next_id] = new_book
        self.next_id += 1
        
        logger.info(f"📚 Created new book: {title} by {author}")
        return new_book.to_dict()
    
    def update_book(self, book_id: int, title: Optional[str] = None, 
                   author: Optional[str] = None, year: Optional[int] = None, 
                   isbn: Optional[str] = None) -> Optional[Dict[str, Union[str, int]]]:
        """
        Update an existing book.
        
        Args:
            book_id (int): ID of the book to update
            title (str, optional): New title
            author (str, optional): New author
            year (int, optional): New year
            isbn (str, optional): New ISBN
            
        Returns:
            Dict or None: Updated book if found, None otherwise ✏️
        """
        book = self.books.get(book_id)
        if not book:
            return None
        
        book.update(title, author, year, isbn)
        logger.info(f"📝 Updated book ID {book_id}")
        return book.to_dict()
    
    def delete_book(self, book_id: int) -> bool:
        """
        Delete a book by ID.
        
        Args:
            book_id (int): ID of the book to delete
            
        Returns:
            bool: True if deleted, False if not found 🗑️
        """
        if book_id in self.books:
            del self.books[book_id]
            logger.info(f"🗑️ Deleted book ID {book_id}")
            return True
        return False


# Initialize Flask app and book manager 🚀
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration
book_manager = BookManager()


@app.errorhandler(404)
def not_found(error) -> tuple:
    """Handle 404 errors with a friendly JSON response."""
    return jsonify({'error': 'Resource not found 😕'}), 404


@app.errorhandler(400)
def bad_request(error) -> tuple:
    """Handle 400 errors with a helpful JSON response."""
    return jsonify({'error': 'Bad request - please check your data 📋'}), 400


@app.route('/health', methods=['GET'])
def health_check() -> tuple:
    """
    🏥 Health check endpoint to verify the API is running.
    
    Returns:
        JSON response with API status and timestamp
    """
    return jsonify({
        'status': 'healthy! 🎉',
        'timestamp': datetime.now().isoformat(),
        'message': 'Flask CRUD API is running smoothly!'
    }), 200


@app.route('/books', methods=['GET'])
def get_all_books() -> tuple:
    """
    📚 GET /books - Retrieve all books in the collection.
    
    Returns:
        JSON response with list of all books and metadata
    """
    books = book_manager.get_all_books()
    
    return jsonify({
        'books': books,
        'count': len(books),
        'message': f'Found {len(books)} books! 📚'
    }), 200


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id: int) -> tuple:
    """
    🔍 GET /books/{id} - Retrieve a specific book by ID.
    
    Args:
        book_id (int): The ID of the book to retrieve
        
    Returns:
        JSON response with book data or error message
    """
    book = book_manager.get_book(book_id)
    
    if not book:
        return jsonify({
            'error': f'Book with ID {book_id} not found 😕',
            'message': 'Please check the book ID and try again'
        }), 404
    
    return jsonify({
        'book': book,
        'message': f'Found book: {book["title"]} 📖'
    }), 200


@app.route('/books', methods=['POST'])
def create_book() -> tuple:
    """
    ✨ POST /books - Create a new book.
    
    Expected JSON payload:
    {
        "title": "Book Title",
        "author": "Author Name", 
        "year": 2023,
        "isbn": "optional-isbn"
    }
    
    Returns:
        JSON response with created book data
    """
    data = request.get_json()
    
    # Validate required fields 📋
    required_fields = ['title', 'author', 'year']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': f'Missing required fields: {", ".join(missing_fields)} 📋',
            'required_fields': required_fields,
            'message': 'Please provide all required fields'
        }), 400
    
    # Validate data types 🔍
    try:
        year = int(data['year'])
    except (ValueError, TypeError):
        return jsonify({
            'error': 'Year must be a valid integer 📅',
            'message': 'Please provide a valid publication year'
        }), 400
    
    # Create the book ✨
    try:
        new_book = book_manager.create_book(
            title=data['title'],
            author=data['author'],
            year=year,
            isbn=data.get('isbn')
        )
        
        return jsonify({
            'book': new_book,
            'message': f'Successfully created book: {new_book["title"]} ✨'
        }), 201
    
    except Exception as e:
        logger.error(f"Error creating book: {str(e)}")
        return jsonify({
            'error': 'Failed to create book 😞',
            'message': 'Please try again or contact support'
        }), 500


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id: int) -> tuple:
    """
    ✏️ PUT /books/{id} - Update an existing book.
    
    Args:
        book_id (int): ID of the book to update
        
    Expected JSON payload (all fields optional):
    {
        "title": "New Title",
        "author": "New Author",
        "year": 2024,
        "isbn": "new-isbn"
    }
    
    Returns:
        JSON response with updated book data
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'No update data provided 📋',
            'message': 'Please provide at least one field to update'
        }), 400
    
    # Validate year if provided 📅
    if 'year' in data:
        try:
            data['year'] = int(data['year'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Year must be a valid integer 📅',
                'message': 'Please provide a valid publication year'
            }), 400
    
    # Update the book ✏️
    updated_book = book_manager.update_book(
        book_id=book_id,
        title=data.get('title'),
        author=data.get('author'),
        year=data.get('year'),
        isbn=data.get('isbn')
    )
    
    if not updated_book:
        return jsonify({
            'error': f'Book with ID {book_id} not found 😕',
            'message': 'Please check the book ID and try again'
        }), 404
    
    return jsonify({
        'book': updated_book,
        'message': f'Successfully updated book: {updated_book["title"]} ✏️'
    }), 200


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id: int) -> tuple:
    """
    🗑️ DELETE /books/{id} - Delete a book by ID.
    
    Args:
        book_id (int): ID of the book to delete
        
    Returns:
        JSON response confirming deletion or error
    """
    success = book_manager.delete_book(book_id)
    
    if not success:
        return jsonify({
            'error': f'Book with ID {book_id} not found 😕',
            'message': 'Cannot delete a book that does not exist'
        }), 404
    
    return jsonify({
        'message': f'Successfully deleted book with ID {book_id} 🗑️',
        'deleted_id': book_id
    }), 200


if __name__ == '__main__':
    """
    🚀 Run the Flask application in development mode.
    
    This will start the server on http://localhost:5000
    Perfect for testing and development!
    """
    print("🚀 Starting Flask CRUD API...")
    print("📚 Books API available at: http://localhost:5000/books")
    print("🏥 Health check at: http://localhost:5000/health")
    
    app.run(
        debug=True,  # Enable debug mode for development
        host='0.0.0.0',  # Allow external connections
        port=5000  # Default Flask port
    )