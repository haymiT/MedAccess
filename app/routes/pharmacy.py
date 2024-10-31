# app/routes/pharmacy.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.models import db, Pharmacy, User
from flask import jsonify

pharmacy_bp = Blueprint('pharmacy_bp', __name__)

# Get all pharmacies
@pharmacy_bp.route('/pharmacies', methods=['GET'])
def get_pharmacies():
    pharmacies = Pharmacy.query.all()
    all_pharmacy= [phar.to_dict() for phar in pharmacies]
    return jsonify(all_pharmacy)
    # return render_template('pharmacy/index.html', pharmacies=pharmacies)

# Get a single pharmacy by ID
@pharmacy_bp.route('/pharmacies/<int:id>', methods=['GET'])
def get_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    pharm = pharmacy.to_dict()
    return jsonify(pharm)
    # return render_template('pharmacy/view.html', pharmacy=pharmacy)



# Create a new pharmacy
@pharmacy_bp.route('/pharmacies/new', methods=['GET', 'POST'])
def create_pharmacy():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        name = data.get('name')
        location = data.get('location')
        phone_number = data.get('phone_number')
        established_year = data.get('established_year')
        license_number = data.get('license_number')
        owner_id = data.get('owner_id')

        new_pharmacy = Pharmacy(
            name=name,
            location=location,
            phone_number=phone_number,
            established_year=established_year,
            license_number=license_number,
            owner_id=owner_id
        )

        try:
            db.session.add(new_pharmacy)
            db.session.commit()
            return jsonify({'message': 'Pharmacy created successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error creating pharmacy: {e}'}), 500

    # Get all users for the owner selection
    users = User.query.all()
    return jsonify({
        'users': [user.to_dict() for user in users]
    }), 200


# Update an existing pharmacy
@pharmacy_bp.route('/pharmacies/<int:id>/edit', methods=['GET', 'POST'])
def update_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        pharmacy.name = data.get('name')
        pharmacy.location = data.get('location')
        pharmacy.phone_number = data.get('phone_number')
        pharmacy.established_year = data.get('established_year')
        pharmacy.license_number = data.get('license_number')
        pharmacy.owner_id = data.get('owner_id')

        try:
            db.session.commit()
            return jsonify({'message': 'Pharmacy updated successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error updating pharmacy: {e}'}), 500

    # Get all users for the owner selection
    users = User.query.all()
    return jsonify({
        'pharmacy': pharmacy.to_dict(),
        'users': [user.to_dict() for user in users]
    }), 200

# Delete a pharmacy
@pharmacy_bp.route('/pharmacies/<int:id>/delete', methods=['POST'])
def delete_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)

    try:
        db.session.delete(pharmacy)
        db.session.commit()
        return jsonify({'message': 'Pharmacy deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting pharmacy: {e}'}), 500