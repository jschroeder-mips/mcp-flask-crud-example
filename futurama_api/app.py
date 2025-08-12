"""
🚀 Futurama Quotes CRUD REST API
==============================

Welcome to the future! This module provides a simple REST API for managing Futurama quotes
with full CRUD operations. Perfect for learning REST API development and MCP server integration!

Good news, everyone! This API lets you manage quotes from your favorite Futurama characters.
Bite my shiny metal API! 🤖

Author: GitHub Copilot 🤖
Date: 2025-01-11
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from typing import Dict, List, Optional, Union
import logging
from datetime import datetime

# Configure logging for better debugging 📊
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FuturamaQuote:
    """
    🤖 Futurama Quote model class for our quote management system.
    
    This class represents a quote from the amazing world of Futurama with properties
    like the quote text, character who said it, episode info, etc.
    Bite my shiny metal class! 🤖
    """
    
    def __init__(
        self,
        quote_id: int,
        text: str,
        character: str,
        episode: str,
        season: Optional[int] = None,
        year: Optional[int] = None,
    ) -> None:
        """
        Initialize a new FuturamaQuote instance.
        
        Args:
            quote_id (int): Unique identifier for the quote 🆔
            text (str): The actual quote text �
            character (str): Character who said the quote 🎭
            episode (str): Episode name or identifier �
            season (int, optional): Season number 📅
            year (int, optional): Year the episode aired 🗓️
        """
        self.id = quote_id
        self.text = text
        self.character = character
        self.episode = episode
        self.season = season
        self.year = year
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Union[str, int, None]]:
        """
        Convert the FuturamaQuote instance to a dictionary for JSON serialization.
        
        Returns:
            Dict: Dictionary representation of the quote 📋
        """
        return {
            'id': self.id,
            'text': self.text,
            'character': self.character,
            'episode': self.episode,
            'season': self.season,
            'year': self.year,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def update(
        self,
        text: Optional[str] = None,
        character: Optional[str] = None,
        episode: Optional[str] = None,
        season: Optional[int] = None,
        year: Optional[int] = None,
    ) -> None:
        """
        Update quote properties and timestamp.
        
        Args:
            text (str, optional): New quote text
            character (str, optional): New character
            episode (str, optional): New episode
            season (int, optional): New season
            year (int, optional): New year
        """
        if text is not None:
            self.text = text
        if character is not None:
            self.character = character
        if episode is not None:
            self.episode = episode
        if season is not None:
            self.season = season
        if year is not None:
            self.year = year
        self.updated_at = datetime.now().isoformat()


class QuoteManager:
    """
    🤖 Simple in-memory Futurama quote storage manager.
    
    This class handles all CRUD operations for quotes. In a real application,
    you'd replace this with a proper database like PostgreSQL or MongoDB!
    But for now, we're keeping it simple like Bender's brain! 🤖
    """
    
    def __init__(self) -> None:
        """Initialize the quote manager with some sample Futurama quotes."""
        self.quotes: Dict[int, FuturamaQuote] = {}
        self.next_id = 1
        self._initialize_sample_data()
    
    def _initialize_sample_data(self) -> None:
        """Add some classic Futurama quotes to get started! �✨"""
        sample_quotes = [
            FuturamaQuote(
                1,
                "Bite my shiny metal ass!",
                "Bender",
                "A Fishful of Dollars",
                1,
                1999,
            ),
            FuturamaQuote(
                2,
                "Good news everyone!",
                "Professor Farnsworth",
                "Various Episodes",
                None,
                None,
            ),
            FuturamaQuote(
                3,
                "Shut up and take my money!",
                "Fry",
                "Attack of the Killer App",
                6,
                2010,
            ),
            FuturamaQuote(
                4,
                "Why not Zoidberg?",
                "Dr. Zoidberg",
                "Various Episodes",
                None,
                None,
            ),
            FuturamaQuote(
                5,
                "I'm going to build my own theme park, with blackjack and hookers!",
                "Bender",
                "Godfellas",
                3,
                2002,
            ),
        ]
        
        for quote in sample_quotes:
            self.quotes[quote.id] = quote
            self.next_id = max(self.next_id, quote.id + 1)
    
    def get_all_quotes(self) -> List[Dict[str, Union[str, int, None]]]:
        """
        Get all quotes in the collection.
        
        Returns:
            List[Dict]: List of all quotes as dictionaries �
        """
        return [quote.to_dict() for quote in self.quotes.values()]
    
    def get_quote(self, quote_id: int) -> Optional[Dict[str, Union[str, int, None]]]:
        """
        Get a specific quote by ID.
        
        Args:
            quote_id (int): The ID of the quote to retrieve
            
        Returns:
            Dict or None: Quote dictionary if found, None otherwise 🔍
        """
        quote = self.quotes.get(quote_id)
        return quote.to_dict() if quote else None
    
    def create_quote(
        self,
        text: str,
        character: str,
        episode: str,
        season: Optional[int] = None,
        year: Optional[int] = None,
    ) -> Dict[str, Union[str, int, None]]:
        """
        Create a new quote.
        
        Args:
            text (str): Quote text
            character (str): Character who said it
            episode (str): Episode name
            season (int, optional): Season number
            year (int, optional): Year aired
            
        Returns:
            Dict: The newly created quote as a dictionary ✨
        """
        new_quote = FuturamaQuote(
            self.next_id, text, character, episode, season, year
        )
        self.quotes[self.next_id] = new_quote
        self.next_id += 1
        
        logger.info(f"🤖 Created new quote: '{text}' by {character}")
        return new_quote.to_dict()
    
    def update_quote(
        self,
        quote_id: int,
        text: Optional[str] = None,
        character: Optional[str] = None,
        episode: Optional[str] = None,
        season: Optional[int] = None,
        year: Optional[int] = None,
    ) -> Optional[Dict[str, Union[str, int, None]]]:
        """
        Update an existing quote.
        
        Args:
            quote_id (int): ID of the quote to update
            text (str, optional): New text
            character (str, optional): New character
            episode (str, optional): New episode
            season (int, optional): New season
            year (int, optional): New year
            
        Returns:
            Dict or None: Updated quote if found, None otherwise ✏️
        """
        quote = self.quotes.get(quote_id)
        if not quote:
            return None
        
        quote.update(text, character, episode, season, year)
        logger.info(f"📝 Updated quote ID {quote_id}")
        return quote.to_dict()
    
    def delete_quote(self, quote_id: int) -> bool:
        """
        Delete a quote by ID.
        
        Args:
            quote_id (int): ID of the quote to delete
            
        Returns:
            bool: True if deleted, False if not found 🗑️
        """
        if quote_id in self.quotes:
            del self.quotes[quote_id]
            logger.info(f"🗑️ Deleted quote ID {quote_id}")
            return True
        return False


# Initialize Flask app and quote manager 🚀
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration
quote_manager = QuoteManager()


# Futurama-themed frontend template 🎨
FRONTEND_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Futurama Quotes API - Good News Everyone!</title>
    <style>
        /* Futurama-inspired CSS */
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #00ff00;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 0 20px #00ff00;
        }
        
        h1 {
            text-align: center;
            color: #ff6b35;
            text-shadow: 0 0 10px #ff6b35;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            text-align: center;
            color: #00ff00;
            margin-bottom: 30px;
            font-style: italic;
        }
        
        .quote-form {
            background: rgba(0, 255, 0, 0.1);
            padding: 20px;
            border: 1px solid #00ff00;
            border-radius: 5px;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            color: #00ff00;
            margin-bottom: 5px;
            font-weight: bold;
        }
        
        input, textarea, select {
            width: 100%;
            padding: 10px;
            background: #000;
            border: 1px solid #00ff00;
            color: #00ff00;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        
        textarea {
            resize: vertical;
            height: 80px;
        }
        
        button {
            background: #ff6b35;
            color: #000;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            margin-right: 10px;
            margin-bottom: 10px;
            transition: all 0.3s;
        }
        
        button:hover {
            background: #ff8c42;
            box-shadow: 0 0 10px #ff6b35;
        }
        
        .quotes-list {
            border: 1px solid #00ff00;
            border-radius: 5px;
            max-height: 500px;
            overflow-y: auto;
        }
        
        .quote-item {
            background: rgba(0, 255, 0, 0.05);
            border-bottom: 1px solid #004400;
            padding: 15px;
            margin: 0;
        }
        
        .quote-text {
            font-size: 1.2em;
            margin-bottom: 10px;
            color: #ffffff;
            font-style: italic;
        }
        
        .quote-meta {
            font-size: 0.9em;
            color: #00ff00;
        }
        
        .quote-actions {
            margin-top: 10px;
        }
        
        .quote-actions button {
            font-size: 0.8em;
            padding: 5px 10px;
        }
        
        .edit-button {
            background: #35a7ff;
        }
        
        .delete-button {
            background: #ff3535;
        }
        
        .status {
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            font-weight: bold;
        }
        
        .success {
            background: rgba(0, 255, 0, 0.2);
            border: 1px solid #00ff00;
            color: #00ff00;
        }
        
        .error {
            background: rgba(255, 0, 0, 0.2);
            border: 1px solid #ff0000;
            color: #ff0000;
        }
        
        .robot-ascii {
            text-align: center;
            color: #666;
            font-size: 0.8em;
            margin: 20px 0;
            white-space: pre;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Futurama Quotes API</h1>
        <p class="subtitle">"Good news everyone! You can now manage Futurama quotes!"</p>
        
        <div class="robot-ascii">
    /[___]\\
   (  o o  )
    >  ^  <
   /|     |\\
  (_|_____|_)</div>
        
        <div class="quote-form">
            <h2>🤖 Add New Quote</h2>
            <form id="quoteForm">
                <div class="form-group">
                    <label for="text">Quote Text:</label>
                    <textarea id="text" name="text" placeholder="Enter the quote here..." required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="character">Character:</label>
                    <input type="text" id="character" name="character" placeholder="e.g., Bender, Fry, Professor..." required>
                </div>
                
                <div class="form-group">
                    <label for="episode">Episode:</label>
                    <input type="text" id="episode" name="episode" placeholder="Episode name or identifier" required>
                </div>
                
                <div class="form-group">
                    <label for="season">Season (optional):</label>
                    <input type="number" id="season" name="season" placeholder="Season number" min="1">
                </div>
                
                <div class="form-group">
                    <label for="year">Year (optional):</label>
                    <input type="number" id="year" name="year" placeholder="Year aired" min="1999" max="2030">
                </div>
                
                <button type="submit">🚀 Add Quote</button>
                <button type="button" onclick="clearForm()">🧹 Clear</button>
                <button type="button" onclick="loadQuotes()">🔄 Refresh</button>
            </form>
        </div>
        
        <div id="status"></div>
        
        <div class="quotes-list">
            <h2>💬 All Quotes</h2>
            <div id="quotesList">Loading quotes...</div>
        </div>
    </div>

    <script>
        let editingQuoteId = null;

        // Load quotes on page load
        document.addEventListener('DOMContentLoaded', loadQuotes);

        async function loadQuotes() {
            try {
                const response = await fetch('/api/quotes');
                const data = await response.json();
                
                const quotesContainer = document.getElementById('quotesList');
                
                if (data.quotes && data.quotes.length > 0) {
                    quotesContainer.innerHTML = data.quotes.map(quote => `
                        <div class="quote-item">
                            <div class="quote-text">"${quote.text}"</div>
                            <div class="quote-meta">
                                <strong>Character:</strong> ${quote.character} | 
                                <strong>Episode:</strong> ${quote.episode}
                                ${quote.season ? ` | <strong>Season:</strong> ${quote.season}` : ''}
                                ${quote.year ? ` | <strong>Year:</strong> ${quote.year}` : ''}
                            </div>
                            <div class="quote-actions">
                                <button class="edit-button" onclick="editQuote(${quote.id})">✏️ Edit</button>
                                <button class="delete-button" onclick="deleteQuote(${quote.id})">🗑️ Delete</button>
                            </div>
                        </div>
                    `).join('');
                } else {
                    quotesContainer.innerHTML = '<p>No quotes found. Add some!</p>';
                }
            } catch (error) {
                showStatus('Error loading quotes: ' + error.message, 'error');
            }
        }

        document.getElementById('quoteForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const quoteData = {
                text: formData.get('text'),
                character: formData.get('character'),
                episode: formData.get('episode'),
                season: formData.get('season') ? parseInt(formData.get('season')) : null,
                year: formData.get('year') ? parseInt(formData.get('year')) : null
            };

            // Remove null values
            Object.keys(quoteData).forEach(key => {
                if (quoteData[key] === null || quoteData[key] === '') {
                    delete quoteData[key];
                }
            });

            try {
                let response;
                if (editingQuoteId) {
                    // Update existing quote
                    response = await fetch(`/api/quotes/${editingQuoteId}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(quoteData)
                    });
                } else {
                    // Create new quote
                    response = await fetch('/api/quotes', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(quoteData)
                    });
                }

                const result = await response.json();
                
                if (response.ok) {
                    showStatus(result.message, 'success');
                    clearForm();
                    loadQuotes();
                } else {
                    showStatus(result.error || 'An error occurred', 'error');
                }
            } catch (error) {
                showStatus('Error: ' + error.message, 'error');
            }
        });

        async function editQuote(id) {
            try {
                const response = await fetch(`/api/quotes/${id}`);
                const data = await response.json();
                
                if (response.ok) {
                    const quote = data.quote;
                    document.getElementById('text').value = quote.text;
                    document.getElementById('character').value = quote.character;
                    document.getElementById('episode').value = quote.episode;
                    document.getElementById('season').value = quote.season || '';
                    document.getElementById('year').value = quote.year || '';
                    
                    editingQuoteId = id;
                    document.querySelector('button[type="submit"]').textContent = '✏️ Update Quote';
                    showStatus(`Editing quote by ${quote.character}`, 'success');
                } else {
                    showStatus(data.error, 'error');
                }
            } catch (error) {
                showStatus('Error loading quote: ' + error.message, 'error');
            }
        }

        async function deleteQuote(id) {
            if (!confirm('Are you sure you want to delete this quote?')) return;
            
            try {
                const response = await fetch(`/api/quotes/${id}`, { method: 'DELETE' });
                const result = await response.json();
                
                if (response.ok) {
                    showStatus(result.message, 'success');
                    loadQuotes();
                } else {
                    showStatus(result.error, 'error');
                }
            } catch (error) {
                showStatus('Error deleting quote: ' + error.message, 'error');
            }
        }

        function clearForm() {
            document.getElementById('quoteForm').reset();
            editingQuoteId = null;
            document.querySelector('button[type="submit"]').textContent = '🚀 Add Quote';
            showStatus('Form cleared', 'success');
        }

        function showStatus(message, type) {
            const statusDiv = document.getElementById('status');
            statusDiv.innerHTML = `<div class="status ${type}">${message}</div>`;
            setTimeout(() => {
                statusDiv.innerHTML = '';
            }, 5000);
        }
    </script>
</body>
</html>
"""


@app.errorhandler(404)
def not_found(error) -> tuple:
    """Handle 404 errors with a Futurama-themed JSON response."""
    return jsonify({'error': 'Resource not found in the year 3000! �'}), 404


@app.errorhandler(400)
def bad_request(error) -> tuple:
    """Handle 400 errors with a helpful Futurama-themed JSON response."""
    return jsonify({'error': 'Bad request - please check your data, meatbag! 🤖'}), 400


@app.route('/', methods=['GET'])
def frontend() -> str:
    """
    🎨 Serve the Futurama-themed frontend interface.
    
    Returns:
        HTML page with the quote management interface
    """
    return render_template_string(FRONTEND_TEMPLATE)


@app.route('/health', methods=['GET'])
def health_check() -> tuple:
    """
    🏥 Health check endpoint to verify the API is running.
    
    Returns:
        JSON response with API status and timestamp
    """
    return jsonify({
        'status': 'All systems operational in the year 3000! 🚀',
        'timestamp': datetime.now().isoformat(),
        'message': 'Futurama Quotes API is running smoother than Bender\'s shiny metal ass!'
    }), 200


@app.route('/api/quotes', methods=['GET'])
def get_all_quotes() -> tuple:
    """
    � GET /api/quotes - Retrieve all quotes in the collection.
    
    Returns:
        JSON response with list of all quotes and metadata
    """
    quotes = quote_manager.get_all_quotes()
    
    return jsonify({
        'quotes': quotes,
        'count': len(quotes),
        'message': f'Found {len(quotes)} quotes from the year 3000! 🤖'
    }), 200


@app.route('/api/quotes/<int:quote_id>', methods=['GET'])
def get_quote(quote_id: int) -> tuple:
    """
    🔍 GET /api/quotes/{id} - Retrieve a specific quote by ID.
    
    Args:
        quote_id (int): The ID of the quote to retrieve
        
    Returns:
        JSON response with quote data or error message
    """
    quote = quote_manager.get_quote(quote_id)
    
    if not quote:
        return jsonify({
            'error': f'Quote with ID {quote_id} not found in the year 3000! �',
            'message': 'Please check the quote ID and try again'
        }), 404
    
    return jsonify({
        'quote': quote,
        'message': f'Found quote by {quote["character"]} �'
    }), 200


@app.route('/api/quotes', methods=['POST'])
def create_quote() -> tuple:
    """
    ✨ POST /api/quotes - Create a new Futurama quote.
    
    Expected JSON payload:
    {
        "text": "Quote text",
        "character": "Character Name", 
        "episode": "Episode Name",
        "season": 1,
        "year": 1999
    }
    
    Returns:
        JSON response with created quote data
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'No JSON data provided, meatbag! 🤖',
            'message': 'Please provide quote data'
        }), 400
    
    # Validate required fields 📋
    required_fields = ['text', 'character', 'episode']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        return jsonify({
            'error': f'Missing required fields: {", ".join(missing_fields)} 📋',
            'required_fields': required_fields,
            'message': 'Please provide all required fields'
        }), 400
    
    # Validate data types for optional fields 🔍
    if 'season' in data and data['season'] is not None:
        try:
            data['season'] = int(data['season'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Season must be a valid integer 📅',
                'message': 'Please provide a valid season number'
            }), 400
    
    if 'year' in data and data['year'] is not None:
        try:
            data['year'] = int(data['year'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Year must be a valid integer 📅',
                'message': 'Please provide a valid year'
            }), 400
    
    # Create the quote ✨
    try:
        new_quote = quote_manager.create_quote(
            text=data['text'],
            character=data['character'],
            episode=data['episode'],
            season=data.get('season'),
            year=data.get('year')
        )
        
        return jsonify({
            'quote': new_quote,
            'message': f'Successfully created quote by {new_quote["character"]} ✨'
        }), 201
    
    except Exception as e:
        logger.error(f"Error creating quote: {str(e)}")
        return jsonify({
            'error': 'Failed to create quote 😞',
            'message': 'Please try again or contact support'
        }), 500


@app.route('/api/quotes/<int:quote_id>', methods=['PUT'])
def update_quote(quote_id: int) -> tuple:
    """
    ✏️ PUT /api/quotes/{id} - Update an existing quote.
    
    Args:
        quote_id (int): ID of the quote to update
        
    Expected JSON payload (all fields optional):
    {
        "text": "New Quote Text",
        "character": "New Character",
        "episode": "New Episode",
        "season": 2,
        "year": 2000
    }
    
    Returns:
        JSON response with updated quote data
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'No update data provided, meatbag! 🤖',
            'message': 'Please provide at least one field to update'
        }), 400
    
    # Validate season if provided 📅
    if 'season' in data and data['season'] is not None:
        try:
            data['season'] = int(data['season'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Season must be a valid integer 📅',
                'message': 'Please provide a valid season number'
            }), 400
    
    # Validate year if provided 📅
    if 'year' in data and data['year'] is not None:
        try:
            data['year'] = int(data['year'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Year must be a valid integer 📅',
                'message': 'Please provide a valid year'
            }), 400
    
    # Update the quote ✏️
    updated_quote = quote_manager.update_quote(
        quote_id=quote_id,
        text=data.get('text'),
        character=data.get('character'),
        episode=data.get('episode'),
        season=data.get('season'),
        year=data.get('year')
    )
    
    if not updated_quote:
        return jsonify({
            'error': f'Quote with ID {quote_id} not found in the year 3000! �',
            'message': 'Please check the quote ID and try again'
        }), 404
    
    return jsonify({
        'quote': updated_quote,
        'message': f'Successfully updated quote by {updated_quote["character"]} ✏️'
    }), 200


@app.route('/api/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id: int) -> tuple:
    """
    🗑️ DELETE /api/quotes/{id} - Delete a quote by ID.
    
    Args:
        quote_id (int): ID of the quote to delete
        
    Returns:
        JSON response confirming deletion or error
    """
    success = quote_manager.delete_quote(quote_id)
    
    if not success:
        return jsonify({
            'error': f'Quote with ID {quote_id} not found in the year 3000! �',
            'message': 'Cannot delete a quote that does not exist'
        }), 404
    
    return jsonify({
        'message': f'Successfully deleted quote with ID {quote_id} 🗑️',
        'deleted_id': quote_id
    }), 200


# Backward compatibility routes for MCP server
@app.route('/quotes', methods=['GET'])
def get_all_quotes_compat() -> tuple:
    """Backward compatibility route for MCP server."""
    return get_all_quotes()


@app.route('/quotes/<int:quote_id>', methods=['GET'])
def get_quote_compat(quote_id: int) -> tuple:
    """Backward compatibility route for MCP server."""
    return get_quote(quote_id)


@app.route('/quotes', methods=['POST'])
def create_quote_compat() -> tuple:
    """Backward compatibility route for MCP server."""
    return create_quote()


@app.route('/quotes/<int:quote_id>', methods=['PUT'])
def update_quote_compat(quote_id: int) -> tuple:
    """Backward compatibility route for MCP server."""
    return update_quote(quote_id)


@app.route('/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote_compat(quote_id: int) -> tuple:
    """Backward compatibility route for MCP server."""
    return delete_quote(quote_id)


def main() -> None:
    """
    🚀 Run the Flask application in development mode.
    
    This will start the server on http://localhost:5000
    Perfect for testing and development in the year 3000!
    """
    print("🚀 Starting Futurama Quotes API...")
    print("� Quotes API available at: http://localhost:5000/api/quotes")
    print("🎨 Frontend available at: http://localhost:5000/")
    print("🏥 Health check at: http://localhost:5000/health")
    print("🤖 Good news everyone! The API is ready to serve quotes from the future!")
    
    app.run(
        debug=True,  # Enable debug mode for development
        host='0.0.0.0',  # Allow external connections
        port=5000  # Default Flask port
    )


if __name__ == '__main__':
    main()