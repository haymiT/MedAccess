# app/models/supplier.py
from app.models import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the supplier
    name = db.Column(db.String(100), nullable=False)  # Name of the supplier
    address = db.Column(db.String(200), nullable=False)  # Address of the supplier
    phone_number = db.Column(db.String(20), nullable=False)  # Phone number of the supplier
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email address (must be unique)
    location = db.Column(db.String(100), nullable=False)  # Location of the supplier

    def __repr__(self):
        return f"<Supplier {self.name}, Location: {self.location}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone_number': self.phone_number,
            'email': self.email,
            'location': self.location
        }