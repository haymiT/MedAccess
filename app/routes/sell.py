# app/routes/sell.py
from flask import Blueprint, request, jsonify
from app.models import db, Sell, SellItem, Inventory, User
from sqlalchemy.exc import SQLAlchemyError

sell_bp = Blueprint('sell', __name__)

# Route to create a new sale
@sell_bp.route('/sell', methods=['POST'])
def create_sale():
    data = request.get_json()
    user_id = data.get('user_id')  # ID of the pharmacy user making the sale
    items = data.get('items')  # List of items to sell (item_id, quantity)

    # Verify that user is a pharmacy
    user = User.query.filter_by(userId=user_id, role='pharmacy').first()
    if not user:
        return jsonify({"error": "User not authorized or does not exist"}), 403

    # Start calculating the total price
    total_price = 0
    sell_items = []

    # Loop over items to calculate total price and verify stock availability
    for item in items:
        inventory_id = item['inventory_id']
        quantity = item['quantity']

        # Get the inventory item and validate stock
        inventory_item = Inventory.query.get(inventory_id)
        if not inventory_item or inventory_item.quantity < quantity:
            return jsonify({"error": f"Insufficient stock for item ID {inventory_id}"}), 400

        # Calculate subtotal for the item and reduce inventory quantity
        unit_price = inventory_item.unit_price
        subtotal = unit_price * quantity
        total_price += subtotal
        inventory_item.quantity -= quantity

        # Create a SellItem entry
        sell_item = SellItem(inventory_id=inventory_id, quantity=quantity, unit_price=unit_price, subtotal=subtotal)
        sell_items.append(sell_item)

    # Create the Sell entry
    new_sale = Sell(pharmacy_id=user.pharmacies[0].id, user_id=user_id, total_price=total_price)
    new_sale.sale_items = sell_items

    try:
        db.session.add(new_sale)
        db.session.commit()
        return jsonify({"message": "Sale completed successfully", "sale_id": new_sale.id}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Failed to complete the sale", "details": str(e)}), 500

# Route to view receipt
@sell_bp.route('/sell/<int:sale_id>/receipt', methods=['GET'])
def get_receipt(sale_id):
    sale = Sell.query.get(sale_id)
    if not sale:
        return jsonify({"error": "Sale not found"}), 404

    receipt_data = {
        "sale_id": sale.id,
        "pharmacy_id": sale.pharmacy_id,
        "user_id": sale.user_id,
        "sale_date": sale.sale_date,
        "total_price": sale.total_price,
        "items": [{"inventory_id": item.inventory_id, "quantity": item.quantity, "unit_price": item.unit_price, "subtotal": item.subtotal} for item in sale.sale_items]
    }
    return jsonify(receipt_data), 200
