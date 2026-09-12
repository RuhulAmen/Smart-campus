from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Ensure the .env next to this file is loaded regardless of working directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the configured frontend origins (comma-separated in .env)
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000')
cors_origins = [origin.strip() for origin in cors_origins.split(',') if origin.strip()]
CORS(app, origins=cors_origins)

# Load configuration from environment variables (with secure fallbacks for development)
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/smart_campus')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_EXPIRATION_HOURS'] = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))

# Initialize MongoDB with fallback for development if DNS/SRV fails
try:
    app.mongo = PyMongo(app)
except Exception as e:
    fallback_uri = 'mongodb://localhost:27017/smart_campus'
    print(f"⚠️ MongoDB connection failed with configured MONGO_URI ({e}). Falling back to local MongoDB: {fallback_uri}")
    app.config['MONGO_URI'] = fallback_uri
    app.mongo = PyMongo(app)

# Absolute path to the frontend directory (independent of the working directory)
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

# Import models and routes
from models import Facility
from routes import register_routes

# Register routes
register_routes(app)

# Seed default data a single time (guarded so it works under any server/entrypoint)
_data_initialized = False


@app.before_request
def initialize_data():
    """Initialize default facilities on the first API request only."""
    global _data_initialized
    if _data_initialized:
        return

    # Don't hold up static file requests (HTML, CSS, JS)
    if not request.path.startswith('/api'):
        return

    _data_initialized = True  # Avoid blocking repeated subsequent requests if DB is offline
    try:
        facility_model = Facility(app.mongo)
        facility_model.initialize_default_facilities()
        print("✅ Default facilities initialized")
    except Exception as e:
        print(f"⚠️ Could not initialize default facilities (DB might be offline): {e}")


# Serve frontend files
@app.route('/')
def serve_frontend():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
