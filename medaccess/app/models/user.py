# app/models/user.py
from app.models import db

class User(db.Model):
    __tablename__ = 'users'
    
    userId = db.Column(db.Integer, primary_key=True)  # Unique identifier for the user
    name = db.Column(db.String(100), nullable=False)  # Name of the user
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email address (must be unique)
    password = db.Column(db.String(64), nullable=False)  # Password of the user
    phone_number = db.Column(db.String(20), nullable=False)  # Phone number of the user
    role = db.Column(db.Enum('customer', 'pharmacy', 'supplier'), nullable=False)  # Role of the user

    def __repr__(self):
        return f"<User {self.name} (Role: {self.role})>"
    def todictt(self):
        return {
            'userId': self.userId,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'role': self.role
        }