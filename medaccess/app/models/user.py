# app/models/user.py
from app.models import db

class User(db.Model):
    __tablename__ = 'users'
    
    userId = db.Column(db.Integer, primary_key=True)  # Unique identifier for the user
    name = db.Column(db.String(100), nullable=False)  # Name of the user
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email address (must be unique)
    phone_number = db.Column(db.String(20), nullable=False)  # Phone number of the user
    role = db.Column(db.Enum('customer', 'pharmacy', 'supplier'), nullable=False)  # Role of the user

    def __repr__(self):
        return f"<User {self.name} (Role: {self.role})>"
