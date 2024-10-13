# app/routes/inventory.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models import db, Inventory, Pharmacy, Medication

inventory_bp = Blueprint('inventory_bp', __name__)

# Get all inventory items
@inventory_bp.route('/inventory', methods=['GET'])
def get_inventory_items():
    inventory_items = Inventory.query.all()
    return render_template('inventory/index.html', inventory_items=inventory_items)

# Get a single inventory item by inventory_id
@inventory_bp.route('/inventory/<int:inventory_id>', methods=['GET'])
def get_inventory_item(inventory_id):
    # Fetch the inventory item based on its ID
    inventory_item = Inventory.query.get_or_404(inventory_id)

    # Fetch related pharmacy and medication for display
    pharmacy = Pharmacy.query.get(inventory_item.pharmacy_id)
    medication = Medication.query.get(inventory_item.medication_id)

    return render_template('inventory/view.html', inventory_item=inventory_item, pharmacy=pharmacy, medication=medication)


# Create a new inventory item
@inventory_bp.route('/inventory/new', methods=['GET', 'POST'])
def create_inventory_item():
    if request.method == 'POST':
        pharmacy_id = request.form['pharmacy_id']
        medication_id = request.form['medication_id']
        quantity = request.form['quantity']
        unit_price = request.form['unit_price']
        manufacturer = request.form['manufacturer']
        manufacturing_date = request.form['manufacturing_date']
        expiration_date = request.form['expiration_date']
        shelf_number = request.form['shelf_number']
        bin_card = request.form.get('bin_card', None)  # Use get() to handle optional fields
        score_card = request.form.get('score_card', None)  # Use get() to handle optional fields
        dosage_unit = request.form['dosage_unit']  # New field for dosage unit
        dosage_value = request.form['dosage_value']  # New field for dosage value

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
            flash('Inventory item created successfully!', 'success')
            return redirect(url_for('inventory_bp.get_inventory_items'))  # Redirect to inventory list
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating inventory item: {e}', 'danger')

    # Get all pharmacies and medications for dropdowns
    pharmacies = Pharmacy.query.all()
    medications = Medication.query.all()
    
    return render_template('inventory/create.html', pharmacies=pharmacies, medications=medications)
# Update an existing inventory item
@inventory_bp.route('/inventory/<int:inventory_id>/edit', methods=['GET', 'POST'])
def update_inventory_item(inventory_id):
    # Fetch the existing inventory item from the database
    inventory_item = Inventory.query.get_or_404(inventory_id)

    if request.method == 'POST':
        # Update fields with new values from the form
        inventory_item.pharmacy_id = request.form['pharmacy_id']
        inventory_item.medication_id = request.form['medication_id']
        inventory_item.quantity = request.form['quantity']
        inventory_item.unit_price = request.form['unit_price']
        inventory_item.manufacturer = request.form['manufacturer']
        inventory_item.manufacturing_date = request.form['manufacturing_date']
        inventory_item.expiration_date = request.form['expiration_date']
        inventory_item.shelf_number = request.form['shelf_number']
        inventory_item.bin_card = request.form.get('bin_card', None)
        inventory_item.score_card = request.form.get('score_card', None)
        inventory_item.dosage_unit = request.form['dosage_unit']  # Updated dosage unit
        inventory_item.dosage_value = request.form['dosage_value']  # Updated dosage value

        try:
            db.session.commit()  # Commit the changes to the database
            flash('Inventory item updated successfully!', 'success')
            return redirect(url_for('inventory_bp.get_inventory_items'))  # Redirect to inventory list
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating inventory item: {e}', 'danger')

    # Fetch all pharmacies and medications for dropdowns
    pharmacies = Pharmacy.query.all()
    medications = Medication.query.all()
    
    return render_template('inventory/update.html', inventory_item=inventory_item, pharmacies=pharmacies, medications=medications)

# Delete an inventory item
@inventory_bp.route('/inventory/<int:inventory_id>/delete', methods=['POST'])
def delete_inventory_item(inventory_id):
    inventory_item = Inventory.query.get_or_404(inventory_id)

    try:
        db.session.delete(inventory_item)
        db.session.commit()
        flash('Inventory item deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting inventory item: {e}', 'danger')

    return redirect(url_for('inventory_bp.get_inventory_items'))  # Corrected endpoint



@inventory_bp.route('/inventory/search', methods=['GET', 'POST'])
def search_medication():
    search_query = request.form.get('search_query') or request.args.get('search_query')
    
    if search_query:
        # Query the database for medications starting with the search_query
        results = db.session.query(Pharmacy, Medication, Inventory)\
            .join(Inventory, Inventory.pharmacy_id == Pharmacy.id)\
            .join(Medication, Inventory.medication_id == Medication.id)\
            .filter(Medication.name.ilike(f"{search_query}%")).distinct().all()

        # Render the partial results for the modal
        return render_template('inventory/search_results_partial.html', results=results)

    return render_template('inventory/search.html')  # Default if no search query is provided



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

    return render_template('inventory/pharmacy_details.html', pharmacy=pharmacy, drugs=drugs)

