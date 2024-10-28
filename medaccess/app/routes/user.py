# app/routes/user.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.models import db, User

user_bp = Blueprint('user_bp', __name__)

# Get all users
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    allUser = [user.to_dict() for user in users]
    return jsonify(allUser)
    # return render_template('user/index.html', users=users)

# Get a single user by userId
@user_bp.route('/users/<int:userId>', methods=['GET'])
def get_user(userId):
    user = User.query.get_or_404(userId)
    usr = user.to_dict()
    return jsonify(usr)
#return render_template('user/view.html', user=user)
from flask import jsonify

# Create a new user
@user_bp.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone_number = data.get('phone_number')
        role = data.get('role')

        new_user = User(
            name=name,
            email=email,
            password=password,
            phone_number=phone_number,
            role=role
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error creating user: {e}'}), 500

    return jsonify({'error': 'Invalid request method'}), 405


# Update an existing user
@user_bp.route('/users/<int:userId>/edit', methods=['GET', 'POST'])
def update_user(userId):
    user = User.query.get_or_404(userId)
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        user.name = data.get('name')
        user.email = data.get('email')
        user.phone_number = data.get('phone_number')
        user.role = data.get('role')

        try:
            db.session.commit()
            return jsonify({'message': 'User updated successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error updating user: {e}'}), 500

    return jsonify(user.to_dict()), 200

# Delete a user
@user_bp.route('/users/<int:userId>/delete', methods=['POST'])
def delete_user(userId):
    user = User.query.get_or_404(userId)

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting user: {e}'}), 500
    
# Filter users by role
@user_bp.route('/users/role/<string:role>', methods=['GET'])
def filter_users_by_role(role):
    users = User.query.filter_by(role=role).all()
    filtered_users = [user.to_dict() for user in users]
    return jsonify(filtered_users), 200

# Filter users by email
@user_bp.route('/users/email/<string:email>', methods=['GET'])
def filter_users_by_email(email):
    users = User.query.filter_by(email=email).all()
    filtered_users = [user.to_dict() for user in users]
    return jsonify(filtered_users), 200

# Filter users by phone number
@user_bp.route('/users/phone/<string:phone_number>', methods=['GET'])
def filter_users_by_phone(phone_number):
    users = User.query.filter_by(phone_number=phone_number).all()
    filtered_users = [user.to_dict() for user in users]
    return jsonify(filtered_users), 200 
