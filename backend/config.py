import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/smart_campus')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'smart_campus')
    
    # JWT Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', '6e95215c434aa56fbc29654035e84b52d001a42b014e5f1b1328eace7ff9c876')
    JWT_EXPIRATION_HOURS = 24
    
    # CORS Settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000')
    
    # Environment
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'