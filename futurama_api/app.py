"""
Simple Futurama Quotes API
=========================
A minimal Flask API for managing Futurama quotes.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging

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
    global next_id
    sample_quotes = [
        {"text": "Bite my shiny metal ass!", "character": "Bender", "episode": "A Fishful of Dollars"},
        {"text": "Good news everyone!", "character": "Professor Farnsworth", "episode": "Various Episodes"},
        {"text": "Shut up and take my money!", "character": "Fry", "episode": "Attack of the Killer App"},
        {"text": "Why not Zoidberg?", "character": "Dr. Zoidberg", "episode": "Various Episodes"},
    ]
    
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