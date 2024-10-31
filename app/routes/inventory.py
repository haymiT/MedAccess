# app/routes/inventory.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models import db, Inventory, Pharmacy, Medication
from flask import jsonify

inventory_bp = Blueprint('inventory_bp', __name__)

# Get all inventory items
@inventory_bp.route('/inventory', methods=['GET'])
def get_inventory_items():
    inventory_items = Inventory.query.all()
    all_inventory_items = [inv.to_dict() for inv in inventory_items]
    return jsonify(all_inventory_items)
    # return render_template('inventory/index.html', inventory_items=inventory_items)

# Get a single inventory item by inventory_id
@inventory_bp.route('/inventory/<int:inventory_id>', methods=['GET'])
def get_inventory_item(inventory_id):
    # Fetch the inventory item based on its ID
    inventory_item = Inventory.query.get_or_404(inventory_id)
    inv = inventory_item.to_dict()
    

    # Fetch related pharmacy and medication for display
    pharmacy = Pharmacy.query.get(inventory_item.pharmacy_id)
    pharm=pharmacy.to_dict()
    medication = Medication.query.get(inventory_item.medication_id)
    med=medication.to_dict()
    return jsonify(inv, pharm, med)

    # return render_template('inventory/view.html', inventory_item=inventory_item, pharmacy=pharmacy, medication=medication)


# Create a new inventory item
@inventory_bp.route('/inventory/new', methods=['GET', 'POST'])
def create_inventory_item():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        pharmacy_id = data.get('pharmacy_id')
        medication_id = data.get('medication_id')
        quantity = data.get('quantity')
        unit_price = data.get('unit_price')
        manufacturer = data.get('manufacturer')
        manufacturing_date = data.get('manufacturing_date')
        expiration_date = data.get('expiration_date')
        shelf_number = data.get('shelf_number')
        bin_card = data.get('bin_card', None)  # Use get() to handle optional fields
        score_card = data.get('score_card', None)  # Use get() to handle optional fields
        dosage_unit = data.get('dosage_unit')  # New field for dosage unit
        dosage_value = data.get('dosage_value')  # New field for dosage value

        new_inventory_item = Inventory(
            pharmacy_id=pharmacy_id,
            medication_id=medication_id,
            quantity=quantity,
            unit_price=unit_price,
            manufacturer=manufacturer,
            manufacturing_date=manufacturing_date,
            expiration_date=expiration_date,
            shelf_number=shelf_number,
            bin_card=bin_card,
            score_card=score_card,
            dosage_unit=dosage_unit,  # Include dosage unit
            dosage_value=dosage_value   # Include dosage value
        )

        try:
            db.session.add(new_inventory_item)
            db.session.commit()
            return jsonify({'message': 'Inventory item created successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error creating inventory item: {e}'}), 500

    # Get all pharmacies and medications for dropdowns
    pharmacies = Pharmacy.query.all()
    medications = Medication.query.all()
    
    return jsonify({
        'pharmacies': [pharmacy.to_dict() for pharmacy in pharmacies],
        'medications': [medication.to_dict() for medication in medications]
    }), 200


# Update an existing inventory item
@inventory_bp.route('/inventory/<int:inventory_id>/edit', methods=['GET', 'POST'])
def update_inventory_item(inventory_id):
    # Fetch the existing inventory item from the database
    inventory_item = Inventory.query.get_or_404(inventory_id)

    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # Update fields with new values from the form
        inventory_item.pharmacy_id = data.get('pharmacy_id')
        inventory_item.medication_id = data.get('medication_id')
        inventory_item.quantity = data.get('quantity')
        inventory_item.unit_price = data.get('unit_price')
        inventory_item.manufacturer = data.get('manufacturer')
        inventory_item.manufacturing_date = data.get('manufacturing_date')
        inventory_item.expiration_date = data.get('expiration_date')
        inventory_item.shelf_number = data.get('shelf_number')
        inventory_item.bin_card = data.get('bin_card', None)
        inventory_item.score_card = data.get('score_card', None)
        inventory_item.dosage_unit = data.get('dosage_unit')  # Updated dosage unit
        inventory_item.dosage_value = data.get('dosage_value')  # Updated dosage value

        try:
            db.session.commit()  # Commit the changes to the database
            return jsonify({'message': 'Inventory item updated successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error updating inventory item: {e}'}), 500

    # Fetch all pharmacies and medications for dropdowns
    pharmacies = Pharmacy.query.all()
    medications = Medication.query.all()
    
    return jsonify({
        'inventory_item': inventory_item.to_dict(),
        'pharmacies': [pharmacy.to_dict() for pharmacy in pharmacies],
        'medications': [medication.to_dict() for medication in medications]
    }), 200


# Delete an inventory item
@inventory_bp.route('/inventory/<int:inventory_id>/delete', methods=['POST'])
def delete_inventory_item(inventory_id):
    inventory_item = Inventory.query.get_or_404(inventory_id)

    try:
        db.session.delete(inventory_item)
        db.session.commit()
        return jsonify({'message': 'Inventory item deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting inventory item: {e}'}), 500


@inventory_bp.route('/inventory/search', methods=['GET', 'POST'])
def search_medication():
    search_query = request.form.get('search_query') or request.args.get('search_query')
    
    if search_query:
        # Query the database for medications starting with the search_query
        results = db.session.query(Pharmacy, Medication, Inventory)\
            .join(Inventory, Inventory.pharmacy_id == Pharmacy.id)\
            .join(Medication, Inventory.medication_id == Medication.id)\
            .filter(Medication.name.ilike(f"{search_query}%")).distinct().all()

        # Convert results to a list of dictionaries
        results_list = [
            {
                'pharmacy': pharmacy.to_dict(),
                'medication': medication.to_dict(),
                'inventory': inventory.to_dict()
            }
            for pharmacy, medication, inventory in results
        ]

        return jsonify(results_list), 200

    return jsonify({'error': 'No search query provided'}), 400


@inventory_bp.route('/pharmacy/<int:pharmacy_id>', methods=['GET'])
def pharmacy_details(pharmacy_id):
    pharmacy = Pharmacy.query.get_or_404(pharmacy_id)
    
    # Check if a specific medication was requested
    medication_id = request.args.get('medication_id', type=int)

    if medication_id:
        # Query only for the selected medication
        drugs = db.session.query(Inventory, Medication)\
            .join(Medication, Inventory.medication_id == Medication.id)\
            .filter(Inventory.pharmacy_id == pharmacy_id, Medication.id == medication_id).all()
    else:
        # Query all drugs at this pharmacy if no specific medication is selected
        drugs = db.session.query(Inventory, Medication)\
            .join(Medication, Inventory.medication_id == Medication.id)\
            .filter(Inventory.pharmacy_id == pharmacy_id).all()

    # Convert results to a list of dictionaries
    drugs_list = [
        {
            'inventory': inventory.to_dict(),
            'medication': medication.to_dict()
        }
        for inventory, medication in drugs
    ]

    return jsonify({
        'pharmacy': pharmacy.to_dict(),
        'drugs': drugs_list
    }), 200

