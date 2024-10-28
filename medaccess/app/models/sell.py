# app/models/sell.py
from app.models import db
from datetime import datetime

class Sell(db.Model):
    __tablename__ = 'sells'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the sale
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('pharmacies.id'), nullable=False)  # Foreign key to Pharmacy
    user_id = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)  # Foreign key to User (seller)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)  # Total price for the sale
    sale_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Date of the sale
    
    # Relationship to sale items
    sale_items = db.relationship('SellItem', backref='sell', lazy=True)  # Associated sale items
    
    # Relationships with Pharmacy and User
    pharmacy = db.relationship('Pharmacy', backref='sales', lazy=True)
    user = db.relationship('User', backref='sales', lazy=True)
