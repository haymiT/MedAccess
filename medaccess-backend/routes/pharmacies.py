from flask import Blueprint, request, jsonify
from models import db, Pharmacy

pharmacies_bp = Blueprint('pharmacies', __name__)

@pharmacies_bp.route('/', methods=['POST'])
def add_pharmacy():
    data = request.get_json()
    new_pharmacy = Pharmacy(
        userID=data['userID'],
        pharmacyName=data['pharmacyName'],
        licenseNumber=data['licenseNumber'],
        openingHours=data['openingHours'],
        location=data['location']
    )
    db.session.add(new_pharmacy)
    db.session.commit()
    return jsonify({"message": "Pharmacy added successfully", "pharmacyID": new_pharmacy.pharmacyID}), 201

@pharmacies_bp.route('/<int:pharmacy_id>', methods=['GET'])
def get_pharmacy(pharmacy_id):
    pharmacy = Pharmacy.query.get_or_404(pharmacy_id)
    return jsonify({
        "pharmacyID": pharmacy.pharmacyID,
        "pharmacyName": pharmacy.pharmacyName,
        "openingHours": pharmacy.openingHours
    })
