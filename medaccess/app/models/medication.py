# app/models/medication.py
from app.models import db
from sqlalchemy import Enum

class Medication(db.Model):
    __tablename__ = 'medications'
    
    # Define the category options
    CATEGORIES = [
        'Gastrointestinal drugs', 'Anti pain drugs', 'ENT Drugs',
        'Anti bacterial/antibiotics', 'Anti Histamines and Anti allergies',
        'Antihelminitics', 'Hypoglycemic', 'CVS drugs', 'NSAID',
        'Dermatological Agents', 'CNS drugs', 'Respiratory drugs',
        'Hormonal Drugs', 'Antiemetics and antiprotozoal drugs',
        'Ophthalmic products', 'Milk and cosmetics', 'CBS drugs'
    ]

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the medication
    name = db.Column(db.String(100), nullable=False)  # Name of the medication
    description = db.Column(db.Text, nullable=False)  # Description of the medication
    category = db.Column(Enum(*CATEGORIES), nullable=False)  # Category of the medication (using Enum)
    dosage = db.Column(db.String(50), nullable=False)  # Dosage information

    def __repr__(self):
        return f"<Medication {self.name}, Category: {self.category}>"
