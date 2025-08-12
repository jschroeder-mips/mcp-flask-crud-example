"""
🧪 Unit Tests for Futurama Quotes API
====================================

Comprehensive tests for our Flask CRUD API to ensure everything works correctly!
These tests cover all endpoints and edge cases. Perfect for learning testing! �

Good news everyone! These tests will verify our API from the year 3000!

Author: GitHub Copilot 🤖
Date: 2025-01-11
"""

import json
import pytest
from futurama_api.app import app, quote_manager


@pytest.fixture
def client():
    """
    🏗️ Create a test client for our Futurama Quotes Flask application.
    
    This fixture provides a test client that we can use to make
    requests to our API during testing. Good news everyone!
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset quote manager for each test
        quote_manager.quotes.clear()
        quote_manager.next_id = 1
        quote_manager._initialize_sample_data()
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
        assert '3000' in data['status']


class TestListQuotesEndpoint:
    """� Tests for listing all Futurama quotes."""
    
    def test_get_all_quotes_success(self, client):
        """Test getting all quotes returns proper structure."""
        response = client.get('/api/quotes')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'quotes' in data
        assert 'count' in data
        assert 'message' in data
        assert isinstance(data['quotes'], list)
        assert data['count'] == len(data['quotes'])
        assert data['count'] > 0  # Sample data should be present
    
    def test_quotes_have_required_fields(self, client):
        """Test that each quote has all required fields."""
        response = client.get('/api/quotes')
        data = response.get_json()
        
        required_fields = ['id', 'text', 'character', 'episode', 'created_at', 'updated_at']
        
        for quote in data['quotes']:
            for field in required_fields:
                assert field in quote, f"Quote missing required field: {field}"


class TestGetQuoteEndpoint:
    """🔍 Tests for getting a specific Futurama quote."""
    
    def test_get_quote_success(self, client):
        """Test getting an existing quote by ID."""
        # First get all quotes to find a valid ID
        all_quotes_response = client.get('/api/quotes')
        quotes = all_quotes_response.get_json()['quotes']
        quote_id = quotes[0]['id']
        
        # Now get the specific quote
        response = client.get(f'/api/quotes/{quote_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'quote' in data
        assert 'message' in data
        assert data['quote']['id'] == quote_id
    
    def test_get_quote_not_found(self, client):
        """Test getting a non-existent quote returns 404."""
        response = client.get('/api/quotes/999')
        
        assert response.status_code == 404
        data = response.get_json()
        
        assert 'error' in data
        assert 'message' in data
        assert '999' in data['error']


class TestCreateQuoteEndpoint:
    """✨ Tests for creating new Futurama quotes."""
    
    def test_create_quote_success(self, client):
        """Test creating a new quote with valid data."""
        new_quote = {
            "text": "I'm back, baby!",
            "character": "Bender",
            "episode": "Test Episode",
            "season": 1,
            "year": 1999
        }
        
        response = client.post('/api/quotes', 
                              data=json.dumps(new_quote),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = response.get_json()
        
        assert 'quote' in data
        assert 'message' in data
        assert data['quote']['text'] == new_quote['text']
        assert data['quote']['character'] == new_quote['character']
        assert data['quote']['episode'] == new_quote['episode']
        assert data['quote']['season'] == new_quote['season']
        assert data['quote']['year'] == new_quote['year']
        assert 'id' in data['quote']
    
    def test_create_quote_without_optional_fields(self, client):
        """Test creating a quote without optional season and year fields."""
        new_quote = {
            "text": "Why not Zoidberg?",
            "character": "Dr. Zoidberg", 
            "episode": "Various Episodes"
        }
        
        response = client.post('/api/quotes',
                              data=json.dumps(new_quote),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = response.get_json()
        
        assert data['quote']['season'] is None
        assert data['quote']['year'] is None
    
    def test_create_quote_missing_required_field(self, client):
        """Test creating a quote without required fields returns 400."""
        incomplete_quote = {
            "text": "Missing Character",
            "episode": "Test Episode"
        }
        
        response = client.post('/api/quotes',
                              data=json.dumps(incomplete_quote),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        
        assert 'error' in data
        assert 'character' in data['error']
    
    def test_create_quote_invalid_season(self, client):
        """Test creating a quote with invalid season type returns 400."""
        invalid_quote = {
            "text": "Test Quote",
            "character": "Test Character",
            "episode": "Test Episode",
            "season": "not-a-season"
        }
        
        response = client.post('/api/quotes',
                              data=json.dumps(invalid_quote),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        
        assert 'error' in data
        assert 'season' in data['error'].lower()
    
    def test_create_quote_no_json_data(self, client):
        """Test creating a quote without JSON data returns 415 (Unsupported Media Type)."""
        response = client.post('/api/quotes')
        
        assert response.status_code == 415


class TestUpdateQuoteEndpoint:
    """✏️ Tests for updating existing Futurama quotes."""
    
    def test_update_quote_success(self, client):
        """Test updating an existing quote with valid data."""
        # Get a quote ID to update
        all_quotes_response = client.get('/api/quotes')
        quotes = all_quotes_response.get_json()['quotes']
        quote_id = quotes[0]['id']
        
        update_data = {
            "text": "Updated Quote Text",
            "character": "Updated Character"
        }
        
        response = client.put(f'/api/quotes/{quote_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'quote' in data
        assert 'message' in data
        assert data['quote']['text'] == update_data['text']
        assert data['quote']['character'] == update_data['character']
        assert data['quote']['id'] == quote_id
    
    def test_update_quote_partial_update(self, client):
        """Test updating only some fields of a quote."""
        # Get a quote ID to update
        all_quotes_response = client.get('/api/quotes')
        quotes = all_quotes_response.get_json()['quotes']
        quote_id = quotes[0]['id']
        original_character = quotes[0]['character']
        
        update_data = {"text": "Only Text Updated"}
        
        response = client.put(f'/api/quotes/{quote_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        # Text should be updated
        assert data['quote']['text'] == update_data['text']
        # Character should remain unchanged
        assert data['quote']['character'] == original_character
    
    def test_update_quote_not_found(self, client):
        """Test updating a non-existent quote returns 404."""
        update_data = {"text": "Updated Text"}
        
        response = client.put('/api/quotes/999',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 404
        data = response.get_json()
        
        assert 'error' in data
        assert '999' in data['error']
    
    def test_update_quote_no_data(self, client):
        """Test updating a quote without data returns 415 (Unsupported Media Type)."""
        # Get a quote ID to update
        all_quotes_response = client.get('/api/quotes')
        quotes = all_quotes_response.get_json()['quotes']
        quote_id = quotes[0]['id']
        
        response = client.put(f'/api/quotes/{quote_id}')
        
        assert response.status_code == 415
        # 415 errors typically don't include JSON response data
    
    def test_update_quote_invalid_season(self, client):
        """Test updating a quote with invalid season returns 400."""
        # Get a quote ID to update
        all_quotes_response = client.get('/api/quotes')
        quotes = all_quotes_response.get_json()['quotes']
        quote_id = quotes[0]['id']
        
        update_data = {"season": "invalid-season"}
        
        response = client.put(f'/api/quotes/{quote_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        
        assert 'error' in data
        assert 'season' in data['error'].lower()


class TestDeleteQuoteEndpoint:
    """🗑️ Tests for deleting Futurama quotes."""
    
    def test_delete_quote_success(self, client):
        """Test deleting an existing quote."""
        # Get a quote ID to delete
        all_quotes_response = client.get('/api/quotes')
        quotes = all_quotes_response.get_json()['quotes']
        quote_id = quotes[0]['id']
        initial_count = len(quotes)
        
        response = client.delete(f'/api/quotes/{quote_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'message' in data
        assert 'deleted_id' in data
        assert data['deleted_id'] == quote_id
        
        # Verify the quote was actually deleted
        updated_quotes_response = client.get('/api/quotes')
        updated_quotes = updated_quotes_response.get_json()['quotes']
        assert len(updated_quotes) == initial_count - 1
        
        # Verify the specific quote is gone
        quote_ids = [quote['id'] for quote in updated_quotes]
        assert quote_id not in quote_ids
    
    def test_delete_quote_not_found(self, client):
        """Test deleting a non-existent quote returns 404."""
        response = client.delete('/api/quotes/999')
        
        assert response.status_code == 404
        data = response.get_json()
        
        assert 'error' in data
        assert '999' in data['error']
    
    def test_delete_quote_and_verify_get_fails(self, client):
        """Test that getting a deleted quote returns 404."""
        # Get a quote ID to delete
        all_quotes_response = client.get('/api/quotes')
        quotes = all_quotes_response.get_json()['quotes']
        quote_id = quotes[0]['id']
        
        # Delete the quote
        delete_response = client.delete(f'/api/quotes/{quote_id}')
        assert delete_response.status_code == 200
        
        # Try to get the deleted quote
        get_response = client.get(f'/api/quotes/{quote_id}')
        assert get_response.status_code == 404


class TestAPIIntegration:
    """🔄 Integration tests that test multiple operations together."""
    
    def test_full_crud_cycle(self, client):
        """Test a complete CRUD cycle: Create, Read, Update, Delete."""
        # Create a new quote ✨
        new_quote = {
            "text": "I'm gonna build my own theme park, with blackjack and hookers!",
            "character": "Bender",
            "episode": "Godfellas",
            "season": 3,
            "year": 2002
        }
        
        create_response = client.post('/api/quotes',
                                    data=json.dumps(new_quote),
                                    content_type='application/json')
        assert create_response.status_code == 201
        created_quote = create_response.get_json()['quote']
        quote_id = created_quote['id']
        
        # Read the quote 🔍
        read_response = client.get(f'/api/quotes/{quote_id}')
        assert read_response.status_code == 200
        read_quote = read_response.get_json()['quote']
        assert read_quote['text'] == new_quote['text']
        
        # Update the quote ✏️
        update_data = {"text": "Updated: I'm gonna build my own theme park!"}
        update_response = client.put(f'/api/quotes/{quote_id}',
                                   data=json.dumps(update_data),
                                   content_type='application/json')
        assert update_response.status_code == 200
        updated_quote = update_response.get_json()['quote']
        assert updated_quote['text'] == update_data['text']
        
        # Delete the quote 🗑️
        delete_response = client.delete(f'/api/quotes/{quote_id}')
        assert delete_response.status_code == 200
        
        # Verify the quote is gone 🔍
        final_read_response = client.get(f'/api/quotes/{quote_id}')
        assert final_read_response.status_code == 404
    
    def test_create_multiple_quotes_and_list(self, client):
        """Test creating multiple quotes and verifying the list endpoint."""
        # Get initial count
        initial_response = client.get('/api/quotes')
        initial_count = initial_response.get_json()['count']
        
        # Create multiple quotes
        quotes_to_create = [
            {"text": "Good news everyone!", "character": "Professor Farnsworth", "episode": "Various"},
            {"text": "Shut up and take my money!", "character": "Fry", "episode": "Attack of the Killer App"},
            {"text": "Why not Zoidberg?", "character": "Dr. Zoidberg", "episode": "Various"}
        ]
        
        created_ids = []
        for quote_data in quotes_to_create:
            response = client.post('/api/quotes',
                                 data=json.dumps(quote_data),
                                 content_type='application/json')
            assert response.status_code == 201
            created_ids.append(response.get_json()['quote']['id'])
        
        # Verify all quotes appear in list
        final_response = client.get('/api/quotes')
        final_data = final_response.get_json()
        
        assert final_data['count'] == initial_count + len(quotes_to_create)
        
        # Verify our created quotes are in the list
        quote_ids_in_list = [quote['id'] for quote in final_data['quotes']]
        for created_id in created_ids:
            assert created_id in quote_ids_in_list


if __name__ == '__main__':
    """
    🚀 Run the tests directly.
    
    Usage:
    python -m pytest tests/tests_test_api.py -v
    """
    pytest.main([__file__, '-v'])
    
    