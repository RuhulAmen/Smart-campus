import os
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId

class Facility:
    def __init__(self, mongo):
        self.mongo = mongo
        db_name = os.getenv('MONGO_DB_NAME', 'smart_campus')
        if hasattr(mongo, 'db') and mongo.db is not None:
            self.collection = mongo.db['facilities']
        elif hasattr(mongo, 'cx') and mongo.cx is not None:
            self.collection = mongo.cx[db_name]['facilities']
        else:
            self.collection = mongo['facilities']
    
    def create_facility(self, name, location, description, status='operational'):
        """Create a new facility"""
        facility = {
            'name': name,
            'location': location,
            'description': description,
            'status': status,  # operational, maintenance, closed
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True
        }
        
        result = self.collection.insert_one(facility)
        return result.inserted_id
    
    def get_all_facilities(self):
        """Get all active facilities"""
        return list(self.collection.find({'is_active': True}))
    
    def get_facility_by_id(self, facility_id):
        """Get facility by ID"""
        try:
            return self.collection.find_one({'_id': ObjectId(facility_id), 'is_active': True})
        except (InvalidId, TypeError):
            return None
    
    def update_facility(self, facility_id, update_data):
        """Update facility information"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(facility_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except (InvalidId, TypeError):
            return False
    
    def update_status(self, facility_id, status):
        """Update facility status"""
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(facility_id)},
                {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except (InvalidId, TypeError):
            return False
    
    def delete_facility(self, facility_id):
        """Soft delete a facility"""
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(facility_id)},
                {'$set': {'is_active': False, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except (InvalidId, TypeError):
            return False
    
    def initialize_default_facilities(self):
        """Initialize default facilities if none exist"""
        if self.collection.count_documents({}) == 0:
            default_facilities = [
                {'name': 'Washrooms', 'location': 'Building A, Floor 1-4', 'description': 'Clean and well-maintained washrooms', 'status': 'operational'},
                {'name': 'Water Coolers', 'location': 'Building A & B', 'description': 'Drinking water coolers with filters', 'status': 'operational'},
                {'name': 'Water Tanks', 'location': 'Main Campus', 'description': 'Main water storage tanks', 'status': 'operational'},
                {'name': 'Library', 'location': 'Building C', 'description': 'Silent study area with books and computers', 'status': 'operational'},
                {'name': 'Medical Room', 'location': 'Building B, Ground Floor', 'description': 'First aid and basic medical services', 'status': 'operational'},
                {'name': 'Xerox Center', 'location': 'Building A, Floor 2', 'description': 'Printing and photocopy services', 'status': 'operational'},
                {'name': 'Cafeteria', 'location': 'Building A, Ground Floor', 'description': 'Food and beverages available', 'status': 'operational'}
            ]
            
            for facility in default_facilities:
                facility['created_at'] = datetime.utcnow()
                facility['updated_at'] = datetime.utcnow()
                facility['is_active'] = True
                self.collection.insert_one(facility)
            
            return True
        return False