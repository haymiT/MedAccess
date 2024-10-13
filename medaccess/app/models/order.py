# app/models/order.py
from app.models import db
from sqlalchemy import Enum
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    
    # Define order status options
    ORDER_STATUSES = [
        'Pending',
        'Completed',
        'Cancelled',
        'Shipped',
        'Delivered'
    ]

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the order
    order_id = db.Column(db.String(100), unique=True, nullable=False)  # Unique order ID
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('pharmacies.id'), nullable=False)  # Foreign key to Pharmacy
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)  # Foreign key to Supplier
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Order date
    order_status = db.Column(Enum(*ORDER_STATUSES), nullable=False)  # Status of the order
    item_name = db.Column(db.String(100), nullable=False)  # Name of the ordered item
    quantity = db.Column(db.Integer, nullable=False)  # Quantity of the ordered item

    # Relationships
    pharmacy = db.relationship('Pharmacy', backref='orders', lazy=True)
    supplier = db.relationship('Supplier', backref='orders', lazy=True)

    def __repr__(self):
        return f"<Order {self.order_id}: {self.item_name} x {self.quantity}, Status: {self.order_status}>"
