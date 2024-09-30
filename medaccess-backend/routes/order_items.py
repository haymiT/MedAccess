from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
# from app import mysql

order_items_bp = Blueprint('order_items', __name__)

@order_items_bp.route('/order_items', methods=['POST'])
@jwt_required()
def create_order_item():
    from app import mysql  # Import inside the function to avoid circular imports
    data = request.get_json()
    cursor = mysql.connection.cursor()

    # Calculate total price
    total_price = float(data['quantity']) * float(data['pricePerUnit'])

    cursor.execute(
        "INSERT INTO order_items (orderID, medicationID, quantity, pricePerUnit, totalPrice) VALUES (%s, %s, %s, %s, %s)",
        (data['orderID'], data['medicationID'], data['quantity'], data['pricePerUnit'], total_price)
    )
    mysql.connection.commit()
    return jsonify(message="Order item created successfully!", order_item_id=cursor.lastrowid), 201

@order_items_bp.route('/order_items', methods=['GET'])
@jwt_required()
def get_order_items():
    from app import mysql  # Import inside the function to avoid circular imports
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM order_items")
    order_items = cursor.fetchall()
    return jsonify(order_items)

@order_items_bp.route('/order_items/<int:id>', methods=['GET'])
@jwt_required()
def get_order_item_by_id(id):
    from app import mysql  # Import inside the function to avoid circular imports
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM order_items WHERE orderItemID = %s", (id,))
    order_item = cursor.fetchone()
    if order_item:
        return jsonify(order_item)
    else:
        return jsonify(message="Order item not found!"), 404

@order_items_bp.route('/order_items/<int:id>', methods=['PUT'])
@jwt_required()
def update_order_item(id):
    from app import mysql  # Import inside the function to avoid circular imports
    data = request.get_json()
    cursor = mysql.connection.cursor()

    # Calculate new total price if price per unit or quantity is changed
    total_price = float(data['quantity']) * float(data['pricePerUnit'])

    cursor.execute(
        "UPDATE order_items SET orderID=%s, medicationID=%s, quantity=%s, pricePerUnit=%s, totalPrice=%s WHERE orderItemID=%s",
        (data['orderID'], data['medicationID'], data['quantity'], data['pricePerUnit'], total_price, id)
    )
    mysql.connection.commit()

    return jsonify(message="Order item updated successfully!")

@order_items_bp.route('/order_items/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_order_item(id):
    from app import mysql  # Import inside the function to avoid circular imports
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM order_items WHERE orderItemID = %s", (id,))
    mysql.connection.commit()
    return jsonify(message="Order item deleted successfully!")
