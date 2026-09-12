import jwt
from functools import wraps
from flask import request, jsonify, current_app
from datetime import datetime, timedelta
from models import User

def generate_token(user_id, email, role):
    """Generate JWT token"""
    payload = {
        'user_id': str(user_id),
        'email': email,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRATION_HOURS'])
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_token(token):
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Decode token
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get user
        user_model = User(current_app.mongo)
        user = user_model.find_by_id(payload['user_id'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 401
        
        # Add user to request context.
        # Drop the password hash: it is `bytes` (not JSON serializable) and must
        # never be handed to a view or serialized into a response.
        user.pop('password', None)
        user['_id'] = str(user['_id'])
        request.current_user = user
        
        return f(user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = getattr(request, 'current_user', None)
        if not current_user and args and isinstance(args[0], dict) and 'role' in args[0]:
            current_user = args[0]

        if not current_user:
            return jsonify({'error': 'Authentication required'}), 401
        
        if current_user.get('role') != 'admin':
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated

def serialize_object_id(obj):
    """Convert ObjectId to string in a document"""
    if '_id' in obj:
        obj['_id'] = str(obj['_id'])
    return obj