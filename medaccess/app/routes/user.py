# app/routes/user.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.models import db, User

user_bp = Blueprint('user_bp', __name__)

# Get all users
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return render_template('user/index.html', users=users)

# Get a single user by userId
@user_bp.route('/users/<int:userId>', methods=['GET'])
def get_user(userId):
    user = User.query.get_or_404(userId)
    return render_template('user/view.html', user=user)

# Create a new user
@user_bp.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        role = request.form['role']

        new_user = User(
            name=name,
            email=email,
            phone_number=phone_number,
            role=role
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('user_bp.get_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {e}', 'danger')

    return render_template('user/create.html')

# Update an existing user
@user_bp.route('/users/<int:userId>/edit', methods=['GET', 'POST'])
def update_user(userId):
    user = User.query.get_or_404(userId)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.phone_number = request.form['phone_number']
        user.role = request.form['role']

        try:
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('user_bp.get_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {e}', 'danger')

    return render_template('user/update.html', user=user)

# Delete a user
@user_bp.route('/users/<int:userId>/delete', methods=['POST'])
def delete_user(userId):
    user = User.query.get_or_404(userId)

    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {e}', 'danger')

    return redirect(url_for('user_bp.get_users'))
