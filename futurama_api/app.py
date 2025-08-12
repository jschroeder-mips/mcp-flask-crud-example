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

from flask import Flask, request, jsonify, render_template
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
    return render_template('index.html')


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