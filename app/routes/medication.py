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
@medication_bp.route('/medications/new', methods=['POST'])
def create_medication():
    if request.method == 'POST':
        # Validate input
        data = request.get_json() if request.is_json else request.form
        
        name = data.get('name')
        description = data.get('description')
        category = data.get('category')
        dosage = data.get('dosage')

        # Validate that all fields are provided
        if not all([name, description, category, dosage]):
            return jsonify({'error': 'All fields are required!'}), 400
        
        # Validate that the category is valid
        valid_categories = Medication.CATEGORIES
        if category not in valid_categories:
            return jsonify({'error': f'Invalid category! Valid categories are: {", ".join(valid_categories)}'}), 400
        
        # Create a new Medication instance
        new_medication = Medication(
            name=name,
            description=description,
            category=category,
            dosage=dosage
        )

        try:
            # Add and commit the new medication to the database
            db.session.add(new_medication)
            db.session.commit()
            return jsonify({'message': 'Medication created successfully!'}), 201
        except Exception as e:
            # Rollback the session in case of an error
            db.session.rollback()
            return jsonify({'error': f'Error creating medication: {str(e)}'}), 500
        



# Update an existing medication
@medication_bp.route('/medications/<int:id>/edit', methods=['GET', 'POST'])
def update_medication(id):
    medication = Medication.query.get_or_404(id)
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        medication.name = data.get('name')
        medication.description = data.get('description')
        medication.category = data.get('category')
        medication.dosage = data.get('dosage')

        try:
            db.session.commit()
            return jsonify({'message': 'Medication updated successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error updating medication: {e}'}), 500

    return jsonify({
        'id': medication.id,
        'name': medication.name,
        'description': medication.description,
        'category': medication.category,
        'dosage': medication.dosage
    }), 200


# Delete a medication
@medication_bp.route('/medications/<int:id>/delete', methods=['POST'])
def delete_medication(id):
    medication = Medication.query.get_or_404(id)

    try:
        db.session.delete(medication)
        db.session.commit()
        return jsonify({'message': 'Medication deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting medication: {e}'}), 500


