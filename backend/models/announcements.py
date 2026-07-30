from datetime import datetime

class Announcement:
    def __init__(self, mongo):
        self.collection = mongo.db.announcements
    
    def create_announcement(self, title, description, priority, category, created_by):
        """Create a new announcement"""
        announcement = {
            'title': title,
            'description': description,
            'priority': priority,  # high, medium, low
            'category': category,
            'created_by': created_by,
            'date': datetime.utcnow().strftime('%Y-%m-%d'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'status': 'active'
        }
        
        result = self.collection.insert_one(announcement)
        return result.inserted_id
    
    def get_all_announcements(self, limit=100, skip=0):
        """Get all active announcements sorted by date"""
        return list(self.collection.find(
            {'status': 'active'}
        ).sort('created_at', -1).skip(skip).limit(limit))
    
    def get_announcement_by_id(self, announcement_id):
        """Get announcement by ID"""
        from bson import ObjectId
        return self.collection.find_one({'_id': ObjectId(announcement_id), 'status': 'active'})
    
    def update_announcement(self, announcement_id, update_data):
        """Update announcement"""
        from bson import ObjectId
        update_data['updated_at'] = datetime.utcnow()
        result = self.collection.update_one(
            {'_id': ObjectId(announcement_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def delete_announcement(self, announcement_id):
        """Soft delete an announcement"""
        from bson import ObjectId
        result = self.collection.update_one(
            {'_id': ObjectId(announcement_id)},
            {'$set': {'status': 'inactive', 'updated_at': datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    def get_recent_announcements(self, limit=5):
        """Get recent announcements"""
        return list(self.collection.find(
            {'status': 'active'}
        ).sort('created_at', -1).limit(limit))
    
    def get_by_priority(self, priority, limit=50):
        """Get announcements by priority"""
        return list(self.collection.find(
            {'status': 'active', 'priority': priority}
        ).sort('created_at', -1).limit(limit))