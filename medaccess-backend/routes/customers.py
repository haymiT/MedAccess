from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
# from app import mysql

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customers', methods=['POST'])
@jwt_required()
def create_customer():
    from app import mysql  # Import inside the function to avoid circular imports
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO customers (userID) VALUES (%s)", (data['userID'],))
    mysql.connection.commit()
    return jsonify(message="Customer created successfully!"), 201

@customers_bp.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    from app import mysql  # Import inside the function to avoid circular imports
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    return jsonify(customers)

@customers_bp.route('/customers/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    from app import mysql  # Import inside the function to avoid circular imports
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE customers SET userID=%s WHERE customerID=%s", (data['userID'], id))
    mysql.connection.commit()
    return jsonify(message="Customer updated successfully!")

@customers_bp.route('/customers/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    from app import mysql  # Import inside the function to avoid circular imports
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM customers WHERE customerID=%s", (id,))
    mysql.connection.commit()
    return jsonify(message="Customer deleted successfully!")
