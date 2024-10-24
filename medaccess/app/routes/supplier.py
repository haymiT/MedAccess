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
    return render_template('supplier/index.html', suppliers=suppliers)

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
        name = request.form['name']
        address = request.form['address']
        phone_number = request.form['phone_number']
        email = request.form['email']
        location = request.form['location']

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
            flash('Supplier created successfully!', 'success')
            return redirect(url_for('supplier_bp.get_suppliers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating supplier: {e}', 'danger')

    return render_template('supplier/create.html')

# Update an existing supplier
@supplier_bp.route('/suppliers/<int:id>/edit', methods=['GET', 'POST'])
def update_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    
    if request.method == 'POST':
        supplier.name = request.form['name']
        supplier.address = request.form['address']
        supplier.phone_number = request.form['phone_number']
        supplier.email = request.form['email']
        supplier.location = request.form['location']

        try:
            db.session.commit()
            flash('Supplier updated successfully!', 'success')
            return redirect(url_for('supplier_bp.get_suppliers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating supplier: {e}', 'danger')

    return render_template('supplier/update.html', supplier=supplier)

# Delete a supplier
@supplier_bp.route('/suppliers/<int:id>/delete', methods=['POST'])
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)

    try:
        db.session.delete(supplier)
        db.session.commit()
        flash('Supplier deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting supplier: {e}', 'danger')

    return redirect(url_for('supplier_bp.get_suppliers'))
