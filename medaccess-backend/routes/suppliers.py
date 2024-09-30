from flask import Blueprint, request, jsonify
from models import db, Supplier

suppliers_bp = Blueprint('suppliers', __name__)

@suppliers_bp.route('/', methods=['POST'])
def add_supplier():
    data = request.get_json()
    new_supplier = Supplier(
        userID=data['userID'],
        supplierName=data['supplierName'],
        licenseNumber=data['licenseNumber'],
        industry=data['industry'],
        location=data['location']
    )
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify({"message": "Supplier added successfully", "supplierID": new_supplier.supplierID}), 201

@suppliers_bp.route('/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return jsonify({
        "supplierID": supplier.supplierID,
        "supplierName": supplier.supplierName,
        "industry": supplier.industry
    })
