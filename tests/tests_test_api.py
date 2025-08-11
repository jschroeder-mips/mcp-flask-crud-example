"""
🧪 Unit Tests for Flask Books API
=================================

Comprehensive tests for our Flask CRUD API to ensure everything works correctly!
These tests cover all endpoints and edge cases. Perfect for learning testing! 📚

Author: GitHub Copilot 🤖
Date: 2025-01-11
"""

import json
import pytest
from flask_api.app import app, book_manager


@pytest.fixture
def client():
    """
    🏗️ Create a test client for our Flask application.
    
    This fixture provides a test client that we can use to make
    requests to our API during testing.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset book manager for each test
        book_manager.books.clear()
        book_manager.next_id = 1
        book_manager._initialize_sample_data()
        yield client


class TestHealthEndpoint:
    """🏥 Tests for the health check endpoint."""
    
    def test_health_check(self, client):
        """Test that health check returns 200 and proper response."""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'status' in data
        assert 'timestamp' in data
        assert 'message' in data
        assert data['status'] == 'healthy! 🎉'


class TestListBooksEndpoint:
    """📚 Tests for listing all books."""
    
    def test_get_all_books_success(self, client):
        """Test getting all books returns proper structure."""
        response = client.get('/books')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'books' in data
        assert 'count' in data
        assert 'message' in data
        assert isinstance(data['books'], list)
        assert data['count'] == len(data['books'])
        assert data['count'] > 0  # Sample data should be present
    
    def test_books_have_required_fields(self, client):
        """Test that each book has all required fields."""
        response = client.get('/books')
        data = response.get_json()
        
        required_fields = ['id', 'title', 'author', 'year', 'created_at', 'updated_at']
        
        for book in data['books']:
            for field in required_fields:
                assert field in book, f"Book missing required field: {field}"


class TestGetBookEndpoint:
    """🔍 Tests for getting a specific book."""
    
    def test_get_book_success(self, client):
        """Test getting an existing book by ID."""
        # First get all books to find a valid ID
        all_books_response = client.get('/books')
        books = all_books_response.get_json()['books']
        book_id = books[0]['id']
        
        # Now get the specific book
        response = client.get(f'/books/{book_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'book' in data
        assert 'message' in data
        assert data['book']['id'] == book_id
    
    def test_get_book_not_found(self, client):
        """Test getting a non-existent book returns 404."""
        response = client.get('/books/999')
        
        assert response.status_code == 404
        data = response.get_json()
        
        assert 'error' in data
        assert 'message' in data
        assert '999' in data['error']


class TestCreateBookEndpoint:
    """✨ Tests for creating new books."""
    
    def test_create_book_success(self, client):
        """Test creating a new book with valid data."""
        new_book = {
            "title": "Test Book",
            "author": "Test Author",
            "year": 2024,
            "isbn": "978-1234567890"
        }
        
        response = client.post('/books', 
                              data=json.dumps(new_book),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = response.get_json()
        
        assert 'book' in data
        assert 'message' in data
        assert data['book']['title'] == new_book['title']
        assert data['book']['author'] == new_book['author']
        assert data['book']['year'] == new_book['year']
        assert data['book']['isbn'] == new_book['isbn']
        assert 'id' in data['book']
    
    def test_create_book_without_isbn(self, client):
        """Test creating a book without optional ISBN field."""
        new_book = {
            "title": "Book Without ISBN",
            "author": "Some Author", 
            "year": 2024
        }
        
        response = client.post('/books',
                              data=json.dumps(new_book),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = response.get_json()
        
        assert data['book']['isbn'] is None
    
    def test_create_book_missing_required_field(self, client):
        """Test creating a book without required fields returns 400."""
        incomplete_book = {
            "title": "Missing Author",
            "year": 2024
        }
        
        response = client.post('/books',
                              data=json.dumps(incomplete_book),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        
        assert 'error' in data
        assert 'author' in data['error']
    
    def test_create_book_invalid_year(self, client):
        """Test creating a book with invalid year type returns 400."""
        invalid_book = {
            "title": "Test Book",
            "author": "Test Author",
            "year": "not-a-year"
        }
        
        response = client.post('/books',
                              data=json.dumps(invalid_book),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        
        assert 'error' in data
        assert 'year' in data['error'].lower()
    
    def test_create_book_no_json_data(self, client):
        """Test creating a book without JSON data returns 400."""
        response = client.post('/books')
        
        assert response.status_code == 400


class TestUpdateBookEndpoint:
    """✏️ Tests for updating existing books."""
    
    def test_update_book_success(self, client):
        """Test updating an existing book with valid data."""
        # Get a book ID to update
        all_books_response = client.get('/books')
        books = all_books_response.get_json()['books']
        book_id = books[0]['id']
        
        update_data = {
            "title": "Updated Title",
            "author": "Updated Author"
        }
        
        response = client.put(f'/books/{book_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'book' in data
        assert 'message' in data
        assert data['book']['title'] == update_data['title']
        assert data['book']['author'] == update_data['author']
        assert data['book']['id'] == book_id
    
    def test_update_book_partial_update(self, client):
        """Test updating only some fields of a book."""
        # Get a book ID to update
        all_books_response = client.get('/books')
        books = all_books_response.get_json()['books']
        book_id = books[0]['id']
        original_author = books[0]['author']
        
        update_data = {"title": "Only Title Updated"}
        
        response = client.put(f'/books/{book_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        # Title should be updated
        assert data['book']['title'] == update_data['title']
        # Author should remain unchanged
        assert data['book']['author'] == original_author
    
    def test_update_book_not_found(self, client):
        """Test updating a non-existent book returns 404."""
        update_data = {"title": "Updated Title"}
        
        response = client.put('/books/999',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 404
        data = response.get_json()
        
        assert 'error' in data
        assert '999' in data['error']
    
    def test_update_book_no_data(self, client):
        """Test updating a book without data returns 400."""
        # Get a book ID to update
        all_books_response = client.get('/books')
        books = all_books_response.get_json()['books']
        book_id = books[0]['id']
        
        response = client.put(f'/books/{book_id}')
        
        assert response.status_code == 400
        data = response.get_json()
        
        assert 'error' in data
    
    def test_update_book_invalid_year(self, client):
        """Test updating a book with invalid year returns 400."""
        # Get a book ID to update
        all_books_response = client.get('/books')
        books = all_books_response.get_json()['books']
        book_id = books[0]['id']
        
        update_data = {"year": "invalid-year"}
        
        response = client.put(f'/books/{book_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        
        assert 'error' in data
        assert 'year' in data['error'].lower()


class TestDeleteBookEndpoint:
    """🗑️ Tests for deleting books."""
    
    def test_delete_book_success(self, client):
        """Test deleting an existing book."""
        # Get a book ID to delete
        all_books_response = client.get('/books')
        books = all_books_response.get_json()['books']
        book_id = books[0]['id']
        initial_count = len(books)
        
        response = client.delete(f'/books/{book_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'message' in data
        assert 'deleted_id' in data
        assert data['deleted_id'] == book_id
        
        # Verify the book was actually deleted
        updated_books_response = client.get('/books')
        updated_books = updated_books_response.get_json()['books']
        assert len(updated_books) == initial_count - 1
        
        # Verify the specific book is gone
        book_ids = [book['id'] for book in updated_books]
        assert book_id not in book_ids
    
    def test_delete_book_not_found(self, client):
        """Test deleting a non-existent book returns 404."""
        response = client.delete('/books/999')
        
        assert response.status_code == 404
        data = response.get_json()
        
        assert 'error' in data
        assert '999' in data['error']
    
    def test_delete_book_and_verify_get_fails(self, client):
        """Test that getting a deleted book returns 404."""
        # Get a book ID to delete
        all_books_response = client.get('/books')
        books = all_books_response.get_json()['books']
        book_id = books[0]['id']
        
        # Delete the book
        delete_response = client.delete(f'/books/{book_id}')
        assert delete_response.status_code == 200
        
        # Try to get the deleted book
        get_response = client.get(f'/books/{book_id}')
        assert get_response.status_code == 404


class TestAPIIntegration:
    """🔄 Integration tests that test multiple operations together."""
    
    def test_full_crud_cycle(self, client):
        """Test a complete CRUD cycle: Create, Read, Update, Delete."""
        # Create a new book ✨
        new_book = {
            "title": "CRUD Test Book",
            "author": "Test Author",
            "year": 2024,
            "isbn": "978-0000000000"
        }
        
        create_response = client.post('/books',
                                    data=json.dumps(new_book),
                                    content_type='application/json')
        assert create_response.status_code == 201
        created_book = create_response.get_json()['book']
        book_id = created_book['id']
        
        # Read the book 🔍
        read_response = client.get(f'/books/{book_id}')
        assert read_response.status_code == 200
        read_book = read_response.get_json()['book']
        assert read_book['title'] == new_book['title']
        
        # Update the book ✏️
        update_data = {"title": "Updated CRUD Test Book"}
        update_response = client.put(f'/books/{book_id}',
                                   data=json.dumps(update_data),
                                   content_type='application/json')
        assert update_response.status_code == 200
        updated_book = update_response.get_json()['book']
        assert updated_book['title'] == update_data['title']
        
        # Delete the book 🗑️
        delete_response = client.delete(f'/books/{book_id}')
        assert delete_response.status_code == 200
        
        # Verify the book is gone 🔍
        final_read_response = client.get(f'/books/{book_id}')
        assert final_read_response.status_code == 404
    
    def test_create_multiple_books_and_list(self, client):
        """Test creating multiple books and verifying the list endpoint."""
        # Get initial count
        initial_response = client.get('/books')
        initial_count = initial_response.get_json()['count']
        
        # Create multiple books
        books_to_create = [
            {"title": "Book 1", "author": "Author 1", "year": 2021},
            {"title": "Book 2", "author": "Author 2", "year": 2022},
            {"title": "Book 3", "author": "Author 3", "year": 2023}
        ]
        
        created_ids = []
        for book_data in books_to_create:
            response = client.post('/books',
                                 data=json.dumps(book_data),
                                 content_type='application/json')
            assert response.status_code == 201
            created_ids.append(response.get_json()['book']['id'])
        
        # Verify all books appear in list
        final_response = client.get('/books')
        final_data = final_response.get_json()
        
        assert final_data['count'] == initial_count + len(books_to_create)
        
        # Verify our created books are in the list
        book_ids_in_list = [book['id'] for book in final_data['books']]
        for created_id in created_ids:
            assert created_id in book_ids_in_list


if __name__ == '__main__':
    """
    🚀 Run the tests directly.
    
    