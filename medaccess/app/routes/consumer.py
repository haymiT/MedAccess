# app/routes/consumer.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models import db, Consumer
from flask import jsonify

consumer_bp = Blueprint('consumer_bp', __name__)

# Get all consumers
@consumer_bp.route('/consumers', methods=['GET'])
def get_consumers():
    consumers = Consumer.query.all()
    all_consumers = [con.to_dict() for con in consumers]
    return jsonify(all_consumers)
    # return render_template('consumer/index.html', consumers=consumers)

# Get a single consumer by ID
@consumer_bp.route('/consumers/<int:id>', methods=['GET'])
def get_consumer(id):
    consumer = Consumer.query.get_or_404(id)
    con = consumer.to_dict()
    return jsonify(con)
    # return render_template('consumer/view.html', consumer=consumer)

# Create a new consumer
@consumer_bp.route('/consumers/new', methods=['GET', 'POST'])
def create_consumer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']

        new_consumer = Consumer(
            name=name,
            email=email,
            phone_number=phone_number
        )

        try:
            db.session.add(new_consumer)
            db.session.commit()
            flash('Consumer created successfully!', 'success')
            return redirect(url_for('consumer_bp.get_consumers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating consumer: {e}', 'danger')

    return render_template('consumer/create.html')

# Update an existing consumer
@consumer_bp.route('/consumers/<int:id>/edit', methods=['GET', 'POST'])
def update_consumer(id):
    consumer = Consumer.query.get_or_404(id)
    
    if request.method == 'POST':
        consumer.name = request.form['name']
        consumer.email = request.form['email']
        consumer.phone_number = request.form['phone_number']

        try:
            db.session.commit()
            flash('Consumer updated successfully!', 'success')
            return redirect(url_for('consumer_bp.get_consumers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating consumer: {e}', 'danger')

    return render_template('consumer/update.html', consumer=consumer)

# Delete a consumer
@consumer_bp.route('/consumers/<int:id>/delete', methods=['POST'])
def delete_consumer(id):
    consumer = Consumer.query.get_or_404(id)

    try:
        db.session.delete(consumer)
        db.session.commit()
        flash('Consumer deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting consumer: {e}', 'danger')

    return redirect(url_for('consumer_bp.get_consumers'))
