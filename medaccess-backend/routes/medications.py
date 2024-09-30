from flask import Blueprint, request, jsonify
from models import db, Medication

medications_bp = Blueprint('medications', __name__)

@medications_bp.route('/', methods=['POST'])
def add_medication():
    data = request.get_json()
    new_medication = Medication(
        medicationAddedBy=data['medicationAddedBy'],
        medicationName=data['medicationName'],
        medicationDescription=data['medicationDescription'],
        medicationDosage=data['medicationDosage'],
        medicationPrice=data['medicationPrice'],
        medicationManufactureDate=data['medicationManufactureDate'],
        medicationExpireDate=data['medicationExpireDate'],
        medicationMadeIn=data['medicationMadeIn']
    )
    db.session.add(new_medication)
    db.session.commit()
    return jsonify({"message": "Medication added successfully", "medicationID": new_medication.medicationID}), 201

@medications_bp.route('/<int:medication_id>', methods=['GET'])
def get_medication(medication_id):
    medication = Medication.query.get_or_404(medication_id)
    return jsonify({
        "medicationID": medication.medicationID,
        "medicationName": medication.medicationName,
        "medicationPrice": medication.medicationPrice
    })
