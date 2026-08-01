from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
from config import Config
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, origins=app.config['CORS_ORIGINS'].split(','))

# Initialize MongoDB
app.mongo = PyMongo(app)

# Import models and routes
from models import Facility
from routes import register_routes

# Register routes
register_routes(app)

# Initialize default data
@app.before_request
def initialize_data():
    """Initialize default data on first request"""
    try:
        facility_model = Facility(app.mongo)
        facility_model.initialize_default_facilities()
        print("✅ Default facilities initialized")
    except Exception as e:
        print(f"⚠️ Error initializing data: {e}")

# Serve frontend files
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)