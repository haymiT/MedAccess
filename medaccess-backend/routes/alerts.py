from flask import Blueprint, request, jsonify
from models import db, Alert

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/', methods=['POST'])
def create_alert():
    data = request.get_json()
    new_alert = Alert(
        pharmacyID=data['pharmacyID'],
        alertType=data['alertType'],
        alertMessage=data['alertMessage']
    )
    db.session.add(new_alert)
    db.session.commit()
    return jsonify({"message": "Alert created successfully", "alertID": new_alert.alertID}), 201
