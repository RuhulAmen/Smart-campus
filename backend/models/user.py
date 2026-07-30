from datetime import datetime
from flask_pymongo import PyMongo
import bcrypt

class User:
    def __init__(self, mongo):
        self.collection = mongo.db.users
    
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
        """Find user by email"""
        return self.collection.find_one({'email': email})
    
    def find_by_id(self, user_id):
        """Find user by ID"""
        from bson import ObjectId
        return self.collection.find_one({'_id': ObjectId(user_id)})
    
    def verify_password(self, email, password):
        """Verify user password"""
        user = self.find_by_email(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return user
        return None
    
    def update_user(self, user_id, update_data):
        """Update user information"""
        from bson import ObjectId
        update_data['updated_at'] = datetime.utcnow()
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def get_all_users(self, limit=100, skip=0):
        """Get all users with pagination"""
        return list(self.collection.find().skip(skip).limit(limit))
    
    def delete_user(self, user_id):
        """Delete a user"""
        from bson import ObjectId
        result = self.collection.delete_one({'_id': ObjectId(user_id)})
        return result.deleted_count > 0