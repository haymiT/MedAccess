from flask import Blueprint, request, jsonify
from models import db, Transaction

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['POST'])
def create_transaction():
    data = request.get_json()
    new_transaction = Transaction(
        orderID=data['orderID'],
        amount=data['amount'],
        paymentMethod=data['paymentMethod'],
        transactionStatus=data['transactionStatus']
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": "Transaction created successfully", "transactionID": new_transaction.transactionID}), 201
