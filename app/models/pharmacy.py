# app/models/pharmacy.py
from app.models import db

class Pharmacy(db.Model):
    __tablename__ = 'pharmacies'
    
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the pharmacy
    name = db.Column(db.String(100), nullable=False)  # Name of the pharmacy
    location = db.Column(db.String(200), nullable=False)  # Location of the pharmacy
    phone_number = db.Column(db.String(20), nullable=False)  # Phone number of the pharmacy
    established_year = db.Column(db.Integer, nullable=False)  # Year the pharmacy was established
    license_number = db.Column(db.String(50), unique=True, nullable=False)  # License number (must be unique)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)  # Foreign key to User model

    # Relationship with the User model (owner)
    owner = db.relationship('User', backref='pharmacies')  # Back reference to access pharmacies from User

    def __repr__(self):
        return f"<Pharmacy {self.name}, Owner ID: {self.owner_id}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'phone_number': self.phone_number,
            'established_year': self.established_year,
            'license_number': self.license_number,
            'owner_id': self.owner_id
        }