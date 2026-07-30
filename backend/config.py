import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/smart_campus')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'smart_campus')
    
    # JWT Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')
    JWT_EXPIRATION_HOURS = 24
    
    # CORS Settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000')
    
    # Environment
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'