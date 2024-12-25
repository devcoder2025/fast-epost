from datetime import datetime
from . import db

class Package(db.Model):
    __tablename__ = 'packages'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='in_warehouse')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Tracking history relationship
    history = db.relationship('PackageHistory', backref='package', lazy=True)
