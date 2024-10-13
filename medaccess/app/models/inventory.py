# app/models/inventory.py
from app.models import db
from datetime import datetime

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    inventory_id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the inventory item
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('pharmacies.id'), nullable=False)  # Foreign key to Pharmacy
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'), nullable=False)  # Foreign key to Medication
    quantity = db.Column(db.Integer, nullable=False)  # Quantity of the medication
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)  # Unit price of the medication
    manufacturer = db.Column(db.String(100), nullable=False)  # Manufacturer of the medication
    manufacturing_date = db.Column(db.Date, nullable=False)  # Manufacturing date
    expiration_date = db.Column(db.Date, nullable=False)  # Expiration date
    shelf_number = db.Column(db.String(50), nullable=True)  # Shelf number where the item is placed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for when the record was created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for when the record was last updated
    bin_card = db.Column(db.String(50), nullable=True)  # Bin card information for inventory management
    score_card = db.Column(db.String(50), nullable=True)  # Score card information for performance tracking
    dosage_unit = db.Column(db.String(20), nullable=False)  # New field for dosage unit
    dosage_value = db.Column(db.Integer, nullable=False)    # New field for dosage value
    # Relationships
    pharmacy = db.relationship('Pharmacy', backref='inventory_items', lazy=True)
    medication = db.relationship('Medication', backref='inventory_items', lazy=True)

    def __repr__(self):
        return f"<Inventory {self.inventory_id}: {self.quantity} units of {self.medication.name} from {self.manufacturer}>"
