from app import db
from config import Config
from datetime import datetime

def get_db():
    from app import db
    return db

class BaseModel(db.Model):
    __abstract__= True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __init__(self, email, password):
        self.email = email
        self.password_hash = password

    def check_password(self, password):
        return self.password_hash == password


    def to_dict(self):
        pass