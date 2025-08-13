"""
Simple Futurama Quotes API
=========================
A minimal Flask API for managing Futurama quotes.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple Flask app
app = Flask(__name__)
CORS(app)

# In-memory storage for quotes
quotes_db = []
next_id = 1

# Sample data
def init_data():
    """Initialize data from JSON file or fallback to sample quotes."""
    global next_id
    
    # Try to load from JSON file first
    json_file = os.path.join(os.path.dirname(__file__), 'futurama_quotes.json')
    
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                quotes_from_json = data.get('quotes', [])
            
            logger.info(f"Loading {len(quotes_from_json)} quotes from JSON file")
            
            for quote_data in quotes_from_json:
                quote = {
                    "id": next_id,
                    "text": quote_data['text'],
                    "character": quote_data['character'],
                    "episode": quote_data.get('episode', 'Unknown'),
                    "season": quote_data.get('season'),
                    "year": quote_data.get('year'),
                    "created_at": datetime.now().isoformat(),
                }
                quotes_db.append(quote)
                next_id += 1
            
            logger.info(f"Successfully loaded {len(quotes_db)} quotes from JSON")
            return
            
        except Exception as e:
            logger.warning(f"Failed to load JSON file: {e}. Falling back to sample data.")
    else:
        logger.info("JSON file not found. Using sample data.")
    
    # Fallback to sample quotes if JSON loading fails
    sample_quotes = [
        {"text": "Bite my shiny metal ass!", "character": "Bender", "episode": "A Fishful of Dollars"},
        {"text": "Good news everyone!", "character": "Professor Farnsworth", "episode": "Various Episodes"},
        {"text": "Shut up and take my money!", "character": "Fry", "episode": "Attack of the Killer App"},
        {"text": "Why not Zoidberg?", "character": "Dr. Zoidberg", "episode": "Various Episodes"},
    ]
    
    logger.info("Loading sample quotes")
    for quote_data in sample_quotes:
        quote = {
            "id": next_id,
            "text": quote_data["text"],
            "character": quote_data["character"],
            "episode": quote_data["episode"],
            "created_at": datetime.now().isoformat(),
        }
        quotes_db.append(quote)
        next_id += 1

# Initialize sample data
init_data()


@app.route('/health')
def health_check():
    """Check if API is working"""
    return jsonify({
        "status": "healthy",
        "message": "Futurama Quotes API is running"
    })


@app.route('/api/quotes', methods=['GET'])
def get_all_quotes():
    """Get all quotes"""
    return jsonify({
        "count": len(quotes_db),
        "quotes": quotes_db
    })


@app.route('/api/quotes/<int:quote_id>', methods=['GET'])
def get_quote(quote_id):
    """Get a specific quote by ID"""
    quote = next((q for q in quotes_db if q['id'] == quote_id), None)
    if quote:
        return jsonify(quote)
    return jsonify({"error": "Quote not found"}), 404


@app.route('/api/quotes', methods=['POST'])
def create_quote():
    """Create a new quote"""
    global next_id
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if not data.get('text') or not data.get('character'):
        return jsonify({"error": "Text and character are required"}), 400
    
    quote = {
        "id": next_id,
        "text": data['text'],
        "character": data['character'],
        "episode": data.get('episode', 'Unknown'),
        "season": data.get('season'),
        "year": data.get('year'),
        "created_at": datetime.now().isoformat(),
    }
    
    quotes_db.append(quote)
    next_id += 1
    
    logger.info(f"Created quote ID {quote['id']}")
    return jsonify(quote), 201


@app.route('/api/quotes/<int:quote_id>', methods=['PUT'])
def update_quote(quote_id):
    """Update an existing quote"""
    quote = next((q for q in quotes_db if q['id'] == quote_id), None)
    if not quote:
        return jsonify({"error": "Quote not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Update fields if provided
    if 'text' in data:
        quote['text'] = data['text']
    if 'character' in data:
        quote['character'] = data['character']
    if 'episode' in data:
        quote['episode'] = data['episode']
    if 'season' in data:
        quote['season'] = data['season']
    if 'year' in data:
        quote['year'] = data['year']
    
    logger.info(f"Updated quote ID {quote_id}")
    return jsonify(quote)


@app.route('/api/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    """Delete a quote"""
    global quotes_db
    quote = next((q for q in quotes_db if q['id'] == quote_id), None)
    if not quote:
        return jsonify({"error": "Quote not found"}), 404
    
    quotes_db = [q for q in quotes_db if q['id'] != quote_id]
    logger.info(f"Deleted quote ID {quote_id}")
    return jsonify({"message": "Quote deleted successfully"})


if __name__ == '__main__':
    print("Starting Futurama Quotes API...")
    print("API available at: http://localhost:5000/api/quotes")
    print("Health check at: http://localhost:5000/health")
    app.run(host='0.0.0.0', port=5000, debug=True)