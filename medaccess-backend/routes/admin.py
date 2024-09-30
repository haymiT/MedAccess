from flask import Blueprint, jsonify
from models import db, Order, Medication

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
def admin_dashboard():
    total_orders = Order.query.count()
    total_medications = Medication.query.count()
    return jsonify({
        "total_orders": total_orders,
        "total_medications": total_medications,
    }), 200
