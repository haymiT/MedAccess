# app/routes/medication.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models import db, Medication
from flask import jsonify

medication_bp = Blueprint('medication_bp', __name__)

# Get all medications
@medication_bp.route('/medications', methods=['GET'])
def get_medications():
    medications = Medication.query.all()
    all_medications = [med.to_dict() for med in medications]
    return jsonify(all_medications)

    # return render_template('medication/index.html', medications=medications)

# Get a single medication by ID
@medication_bp.route('/medications/<int:id>', methods=['GET'])
def get_medication(id):
    medication = Medication.query.get_or_404(id)
    med = medication.to_dict()
    return jsonify(med)

    # return render_template('medication/view.html', medication=medication)

# Create a new medication
@medication_bp.route('/medications/new', methods=['GET', 'POST'])
def create_medication():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        dosage = request.form['dosage']

        new_medication = Medication(
            name=name,
            description=description,
            category=category,
            dosage=dosage
        )

        try:
            db.session.add(new_medication)
            db.session.commit()
            flash('Medication created successfully!', 'success')
            return redirect(url_for('medication_bp.get_medications'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating medication: {e}', 'danger')

    return render_template('medication/create.html')

# Update an existing medication
@medication_bp.route('/medications/<int:id>/edit', methods=['GET', 'POST'])
def update_medication(id):
    medication = Medication.query.get_or_404(id)
    
    if request.method == 'POST':
        medication.name = request.form['name']
        medication.description = request.form['description']
        medication.category = request.form['category']
        medication.dosage = request.form['dosage']

        try:
            db.session.commit()
            flash('Medication updated successfully!', 'success')
            return redirect(url_for('medication_bp.get_medications'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating medication: {e}', 'danger')

    return render_template('medication/update.html', medication=medication)

# Delete a medication
@medication_bp.route('/medications/<int:id>/delete', methods=['POST'])
def delete_medication(id):
    medication = Medication.query.get_or_404(id)

    try:
        db.session.delete(medication)
        db.session.commit()
        flash('Medication deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting medication: {e}', 'danger')

    return redirect(url_for('medication_bp.get_medications'))
