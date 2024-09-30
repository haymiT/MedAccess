from flask import Blueprint, request, jsonify
from models import db, Order, OrderItem

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(
        userID=data['userID'],
        recipientID=data['recipientID'],
        orderType=data['orderType'],
        totalAmount=data['totalAmount']
    )
    db.session.add(new_order)
    db.session.commit()

    for item in data['items']:
        order_item = OrderItem(
            orderID=new_order.orderID,
            medicationID=item['medicationID'],
            quantity=item['quantity'],
            pricePerUnit=item['pricePerUnit'],
            totalPrice=item['totalPrice']
        )
        db.session.add(order_item)

    db.session.commit()
    return jsonify({"message": "Order created successfully", "orderID": new_order.orderID}), 201

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({
        "orderID": order.orderID,
        "userID": order.userID,
        "recipientID": order.recipientID,
        "totalAmount": order.totalAmount,
        "orderDate": order.orderDate,
        "orderStatus": order.orderStatus
    })
