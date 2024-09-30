from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
# from app import mysql

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory', methods=['POST'])
@jwt_required()
def create_inventory_item():
    from app import mysql  # Import inside the function to avoid circular imports
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO inventory (pharmacyID, medicationID, quantity, reorderLevel, pricePerUnit) VALUES (%s, %s, %s, %s, %s)",
                   (data['pharmacyID'], data['medicationID'], data['quantity'], data['reorderLevel'], data['pricePerUnit']))
    mysql.connection.commit()
    return jsonify(message="Inventory item created successfully!"), 201

@inventory_bp.route('/inventory', methods=['GET'])
@jwt_required()
def get_inventory():
    from app import mysql  # Import inside the function to avoid circular imports
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()
    return jsonify(inventory)

@inventory_bp.route('/inventory/<int:id>', methods=['PUT'])
@jwt_required()
def update_inventory_item(id):
    from app import mysql  # Import inside the function to avoid circular imports
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE inventory SET quantity=%s, reorderLevel=%s, pricePerUnit=%s WHERE inventoryID=%s",
                   (data['quantity'], data['reorderLevel'], data['pricePerUnit'], id))
    mysql.connection.commit()
    return jsonify(message="Inventory item updated successfully!")

@inventory_bp.route('/inventory/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_inventory_item(id):
    from app import mysql  # Import inside the function to avoid circular imports
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM inventory WHERE inventoryID=%s", (id,))
    mysql.connection.commit()
    return jsonify(message="Inventory item deleted successfully!")
