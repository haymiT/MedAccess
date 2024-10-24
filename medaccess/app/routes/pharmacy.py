# app/routes/pharmacy.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.models import db, Pharmacy, User

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
        name = request.form['name']
        location = request.form['location']
        phone_number = request.form['phone_number']
        established_year = request.form['established_year']
        license_number = request.form['license_number']
        owner_id = request.form['owner_id']

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
            flash('Pharmacy created successfully!', 'success')
            return redirect(url_for('pharmacy_bp.get_pharmacies'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating pharmacy: {e}', 'danger')

    # Get all users for the owner selection
    users = User.query.all()
    return render_template('pharmacy/create.html', users=users)

# Update an existing pharmacy
@pharmacy_bp.route('/pharmacies/<int:id>/edit', methods=['GET', 'POST'])
def update_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    if request.method == 'POST':
        pharmacy.name = request.form['name']
        pharmacy.location = request.form['location']
        pharmacy.phone_number = request.form['phone_number']
        pharmacy.established_year = request.form['established_year']
        pharmacy.license_number = request.form['license_number']
        pharmacy.owner_id = request.form['owner_id']

        try:
            db.session.commit()
            flash('Pharmacy updated successfully!', 'success')
            return redirect(url_for('pharmacy_bp.get_pharmacies'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating pharmacy: {e}', 'danger')

    # Get all users for the owner selection
    users = User.query.all()
    return render_template('pharmacy/update.html', pharmacy=pharmacy, users=users)

# Delete a pharmacy
@pharmacy_bp.route('/pharmacies/<int:id>/delete', methods=['POST'])
def delete_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)

    try:
        db.session.delete(pharmacy)
        db.session.commit()
        flash('Pharmacy deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting pharmacy: {e}', 'danger')

    return redirect(url_for('pharmacy_bp.get_pharmacies'))
