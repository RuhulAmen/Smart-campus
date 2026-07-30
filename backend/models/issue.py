from datetime import datetime

class Issue:
    def __init__(self, mongo):
        self.collection = mongo.db.issues
    
    def create_issue(self, facility, title, description, reporter_name, reporter_email):
        """Create a new issue report"""
        issue = {
            'facility': facility,
            'title': title,
            'description': description,
            'reporter_name': reporter_name,
            'reporter_email': reporter_email,
            'status': 'pending',  # pending, in_progress, resolved, rejected
            'date': datetime.utcnow().strftime('%Y-%m-%d'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(issue)
        return result.inserted_id
    
    def get_all_issues(self, limit=100, skip=0):
        """Get all issues sorted by date"""
        return list(self.collection.find().sort('created_at', -1).skip(skip).limit(limit))
    
    def get_issue_by_id(self, issue_id):
        """Get issue by ID"""
        from bson import ObjectId
        return self.collection.find_one({'_id': ObjectId(issue_id)})
    
    def update_issue_status(self, issue_id, status):
        """Update issue status"""
        from bson import ObjectId
        result = self.collection.update_one(
            {'_id': ObjectId(issue_id)},
            {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    def get_issues_by_facility(self, facility):
        """Get issues for a specific facility"""
        return list(self.collection.find({'facility': facility}).sort('created_at', -1))
    
    def get_pending_issues(self):
        """Get all pending issues"""
        return list(self.collection.find({'status': 'pending'}).sort('created_at', -1))
    
    def get_issue_stats(self):
        """Get issue statistics"""
        pipeline = [
            {'$group': {
                '_id': '$status',
                'count': {'$sum': 1}
            }}
        ]
        stats = list(self.collection.aggregate(pipeline))
        
        result = {
            'pending': 0,
            'in_progress': 0,
            'resolved': 0,
            'rejected': 0
        }
        
        for stat in stats:
            result[stat['_id']] = stat['count']
        
        result['total'] = self.collection.count_documents({})
        return result