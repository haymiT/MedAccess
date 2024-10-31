# app/models/sell_item.py
from app.models import db

class SellItem(db.Model):
    __tablename__ = 'sell_items'

    id = db.Column(db.Integer, primary_key=True)
    sell_id = db.Column(db.Integer, db.ForeignKey('sells.id'), nullable=False)  # Foreign key to Sell
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.inventory_id'), nullable=False)  # Foreign key to Inventory
    quantity = db.Column(db.Integer, nullable=False)  # Quantity sold
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)  # Unit price at sale time
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)  # Subtotal for this item (quantity * unit_price)

    # Relationship with Inventory
    inventory = db.relationship('Inventory', backref='sell_items', lazy=True)
