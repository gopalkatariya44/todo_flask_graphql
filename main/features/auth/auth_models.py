import uuid
from datetime import datetime

from sqlalchemy import String, Boolean

from main import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', String(36), primary_key=True, default=str(uuid.uuid4()))
    is_pro = db.Column('is_pro', Boolean, nullable=False, default=False)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self):
        db.create_all()
