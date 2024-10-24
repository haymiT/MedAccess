# app/routes/order.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.models import db, Order, Pharmacy, Supplier

order_bp = Blueprint('order_bp', __name__)

# Get all orders
@order_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    all_orders= [order.to_dict() for order in orders]
    return jsonify(all_orders)
    # return render_template('order/index.html', orders=orders)

# Get a single order by order_id
@order_bp.route('/orders/<string:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first_or_404()
    ord = order.to_dict()
    return jsonify(ord)
    # return render_template('order/view.html', order=order)

# Create a new order
@order_bp.route('/orders/new', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        order_id = request.form['order_id']
        pharmacy_id = request.form['pharmacy_id']
        supplier_id = request.form['supplier_id']
        order_date = request.form['order_date']
        order_status = request.form['order_status']
        item_name = request.form['item_name']
        quantity = request.form['quantity']

        new_order = Order(
            order_id=order_id,
            pharmacy_id=pharmacy_id,
            supplier_id=supplier_id,
            order_date=order_date,
            order_status=order_status,
            item_name=item_name,
            quantity=quantity
        )

        try:
            db.session.add(new_order)
            db.session.commit()
            flash('Order created successfully!', 'success')
            return redirect(url_for('order_bp.get_orders'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating order: {e}', 'danger')

    # Get required data for the form
    pharmacies = Pharmacy.query.all()
    suppliers = Supplier.query.all()
    
    return render_template('order/create.html', pharmacies=pharmacies, suppliers=suppliers)

# Update an existing order
@order_bp.route('/orders/<string:order_id>/edit', methods=['GET', 'POST'])
def update_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first_or_404()
    if request.method == 'POST':
        order.pharmacy_id = request.form['pharmacy_id']
        order.supplier_id = request.form['supplier_id']
        order.order_date = request.form['order_date']
        order.order_status = request.form['order_status']
        order.item_name = request.form['item_name']
        order.quantity = request.form['quantity']

        try:
            db.session.commit()
            flash('Order updated successfully!', 'success')
            return redirect(url_for('order_bp.get_orders'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating order: {e}', 'danger')

    # Get required data for the form
    pharmacies = Pharmacy.query.all()
    suppliers = Supplier.query.all()

    return render_template('order/update.html', order=order, pharmacies=pharmacies, suppliers=suppliers)

# Delete an order
@order_bp.route('/orders/<string:order_id>/delete', methods=['POST'])
def delete_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first_or_404()

    try:
        db.session.delete(order)
        db.session.commit()
        flash('Order deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting order: {e}', 'danger')

    return redirect(url_for('order_bp.get_orders'))
