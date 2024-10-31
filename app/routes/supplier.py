# app/routes/supplier.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models import db, Supplier

supplier_bp = Blueprint('supplier_bp', __name__)

# Get all suppliers
@supplier_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    all_supplier = [sup.to_dict() for sup in suppliers]
    return jsonify(all_supplier)
    # return render_template('supplier/index.html', suppliers=suppliers)

# Get a single supplier by ID
from flask import jsonify
@supplier_bp.route('/suppliers/<int:id>', methods=['GET'])
def get_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    sup = supplier.to_dict()
    return jsonify(sup)
    #return render_template('supplier/view.html', supplier=supplier)

# Create a new supplier
@supplier_bp.route('/suppliers/new', methods=['GET', 'POST'])
def create_supplier():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        name = data.get('name')
        address = data.get('address')
        phone_number = data.get('phone_number')
        email = data.get('email')
        location = data.get('location')

        new_supplier = Supplier(
            name=name,
            address=address,
            phone_number=phone_number,
            email=email,
            location=location
        )

        try:
            db.session.add(new_supplier)
            db.session.commit()
            return jsonify({'message': 'Supplier created successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error creating supplier: {e}'}), 500

    return jsonify({'error': 'Invalid request method'}), 405

# Update an existing supplier
@supplier_bp.route('/suppliers/<int:id>/edit', methods=['GET', 'POST'])
def update_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        supplier.name = data.get('name')
        supplier.address = data.get('address')
        supplier.phone_number = data.get('phone_number')
        supplier.email = data.get('email')
        supplier.location = data.get('location')

        try:
            db.session.commit()
            return jsonify({'message': 'Supplier updated successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error updating supplier: {e}'}), 500

    return jsonify(supplier.to_dict()), 200

# Delete a supplier
@supplier_bp.route('/suppliers/<int:id>/delete', methods=['POST'])
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)

    try:
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({'message': 'Supplier deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting supplier: {e}'}), 500