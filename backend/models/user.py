import os
import re
from datetime import datetime
import bcrypt
from bson import ObjectId
from bson.errors import InvalidId


class User:
    def __init__(self, mongo):
        self.mongo = mongo
        db_name = os.getenv('MONGO_DB_NAME', 'smart_campus')
        if hasattr(mongo, 'db') and mongo.db is not None:
            self.collection = mongo.db['users']
        elif hasattr(mongo, 'cx') and mongo.cx is not None:
            self.collection = mongo.cx[db_name]['users']
        else:
            self.collection = mongo['users']

    def create_user(self, full_name, email, student_id, password, role='student'):
        """Create a new user with hashed password"""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = {
            'full_name': full_name,
            'email': email,
            'student_id': student_id,
            'password': hashed_password,
            'role': role,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True
        }

        result = self.collection.insert_one(user)
        return result.inserted_id

    def find_by_email(self, email):
        """Find user by email (case-insensitive)"""
        if not email:
            return None
        return self.collection.find_one({
            'email': re.compile('^' + re.escape(str(email).strip()) + '$', re.IGNORECASE)
        })

    def find_by_student_id(self, student_id):
        """Find user by student ID"""
        if not student_id:
            return None
        return self.collection.find_one({'student_id': str(student_id).strip()})

    def find_by_id(self, user_id):
        """Find user by ID"""
        try:
            return self.collection.find_one({'_id': ObjectId(user_id)})
        except (InvalidId, TypeError):
            return None

    def verify_password(self, email, password):
        """Verify user password"""
        user = self.find_by_email(email)
        if not user or not password:
            return None
        user_pw = user.get('password')
        if isinstance(user_pw, str):
            user_pw = user_pw.encode('utf-8')
        elif user_pw is not None:
            user_pw = bytes(user_pw)
        else:
            return None

        if bcrypt.checkpw(str(password).encode('utf-8'), user_pw):
            return user
        return None

    def update_user(self, user_id, update_data):
        """Update user information"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except (InvalidId, TypeError):
            return False

    def get_all_users(self, limit=100, skip=0):
        """Get all users with pagination"""
        return list(self.collection.find().skip(skip).limit(limit))

    def delete_user(self, user_id):
        """Delete a user"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(user_id)})
            return result.deleted_count > 0
        except (InvalidId, TypeError):
            return False
