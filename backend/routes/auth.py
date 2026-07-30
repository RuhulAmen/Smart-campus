from flask import Blueprint, request, jsonify, session
from models import User
from utils.helpers import generate_token, token_required
from datetime import datetime
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """User registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['full_name', 'email', 'student_id', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Get user model instance
        user_model = User(auth_bp.mongo)
        
        # Check if user already exists
        existing_user = user_model.find_by_email(data['email'])
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create user
        user_id = user_model.create_user(
            full_name=data['full_name'],
            email=data['email'],
            student_id=data['student_id'],
            password=data['password'],
            role=data.get('role', 'student')
        )
        
        # Get created user
        user = user_model.find_by_id(user_id)
        user.pop('password', None)  # Remove password from response
        
        # Generate token
        token = generate_token(str(user['_id']), user['email'], user['role'])
        
        return jsonify({
            'message': 'User created successfully',
            'user': user,
            'token': token
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400
        
        user_model = User(auth_bp.mongo)
        user = user_model.find_by_email(data['email'])
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate token
        token = generate_token(str(user['_id']), user['email'], user['role'])
        
        # Remove password from response
        user.pop('password', None)
        user['_id'] = str(user['_id'])
        
        return jsonify({
            'message': 'Login successful',
            'user': user,
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """User logout"""
    try:
        # Clear session
        session.clear()
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify', methods=['GET'])
@token_required
def verify_token(current_user):
    """Verify token and get current user"""
    try:
        return jsonify({
            'user': current_user,
            'authenticated': True
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get user profile"""
    try:
        user_model = User(auth_bp.mongo)
        user = user_model.find_by_id(current_user['_id'])
        user.pop('password', None)
        user['_id'] = str(user['_id'])
        
        return jsonify({'user': user}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update user profile"""
    try:
        data = request.get_json()
        user_model = User(auth_bp.mongo)
        
        # Update user
        update_data = {}
        allowed_fields = ['full_name', 'email', 'student_id']
        
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        # Update password if provided
        if 'password' in data and data['password']:
            hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            update_data['password'] = hashed
        
        if update_data:
            user_model.update_user(current_user['_id'], update_data)
        
        # Get updated user
        user = user_model.find_by_id(current_user['_id'])
        user.pop('password', None)
        user['_id'] = str(user['_id'])
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500