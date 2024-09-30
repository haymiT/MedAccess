from flask import Blueprint, request, jsonify
from models import db, Delivery

delivery_bp = Blueprint('delivery', __name__)

@delivery_bp.route('/', methods=['POST'])
def create_delivery():
    data = request.get_json()
    new_delivery = Delivery(
        orderID=data['orderID'],
        deliveryStatus=data['deliveryStatus'],
        deliveryAddress=data['deliveryAddress'],
        trackingNumber=data['trackingNumber']
    )
    db.session.add(new_delivery)
    db.session.commit()
    return jsonify({"message": "Delivery created successfully", "deliveryID": new_delivery.deliveryID}), 201
