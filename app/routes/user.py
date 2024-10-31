# app/routes/user.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.models import db, User, Supplier

user_bp = Blueprint('user_bp', __name__)

# Get all users
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.filter_by(is_archived=False).all()
    allUser = [user.to_dict() for user in users]
    return jsonify(allUser)


# Get a single user by userId
@user_bp.route('/users/<int:userId>', methods=['GET'])
def get_user(userId):
    user = User.query.get_or_404(userId)
    usr = user.to_dict()
    return jsonify(usr)
#return render_template('user/view.html', user=user)

import bcrypt
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

        # Input validation
        if not name or not email or not password or not phone_number or not role:
            return jsonify({'error': 'All fields are required.'}), 400
        
        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long.'}), 400

        if role not in ['customer', 'pharmacy', 'supplier']:
            return jsonify({'error': 'Invalid role specified.'}), 400

        # Check for existing user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already in use.'}), 400

        # Encrypt the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create a new User instance
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            phone_number=phone_number,
            role=role
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            # If the user role is 'supplier', insert into the suppliers table
            if role == 'supplier':
                new_supplier = Supplier(
                    name=name,
                    address='Default Address',  # Modify this as needed
                    phone_number=phone_number,
                    email=email,
                    location='Default Location'  # Modify this as needed
                )
                db.session.add(new_supplier)
                db.session.commit()

            return jsonify({'message': 'User created successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error creating user: {str(e)}'}), 500

    return jsonify({'error': 'Invalid request method. Use POST to create a user.'}), 405


# Update an existing user
@user_bp.route('/users/<int:userId>', methods=['PUT'])
def update_user(userId):
    user = User.query.get_or_404(userId)

    # Retrieve JSON data from the request
    data = request.get_json() if request.is_json else request.form

    # Update user attributes
    user.name = data.get('name', user.name)  
    user.email = data.get('email', user.email)
    user.phone_number = data.get('phone_number', user.phone_number)
    new_role = data.get('role', user.role)  
    old_role = user.role

    # Encrypt the password if it is being updated
    if 'password' in data and data['password']:  
        user.password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        user.role = new_role
        db.session.commit()

        # Handle supplier role updates
        if new_role == 'supplier':
            supplier = Supplier.query.filter_by(email=user.email).first()
            if supplier:
                # Update existing supplier information
                supplier.name = user.name
                supplier.phone_number = user.phone_number
                supplier.address = 'Default Address'  # Modify as needed
                supplier.location = 'Default Location'  # Modify as needed
            else:
                # Create a new supplier
                new_supplier = Supplier(
                    name=user.name,
                    address='Default Address',  # Modify as needed
                    phone_number=user.phone_number,
                    email=user.email,
                    location='Default Location'  # Modify as needed
                )
                db.session.add(new_supplier)

        elif old_role == 'supplier' and new_role != 'supplier':
            # If the role changed from 'supplier' to another role, delete from suppliers table
            supplier = Supplier.query.filter_by(email=user.email).first()
            if supplier:
                db.session.delete(supplier)

        # Commit the changes after processing suppliers
        db.session.commit()

        return jsonify({'message': 'User updated successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating user: {str(e)}'}), 500


# soft delete a user
@user_bp.route('/users/<int:userId>/archive', methods=['DElETE'])
def archive_user(userId):
    user = User.query.get_or_404(userId)

    try:
        user.is_archived = True
        db.session.commit()
        return jsonify({'message': 'User archived successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error archiving user: {e}'}), 500

# Restore an archived user
@user_bp.route('/users/<int:userId>/restore', methods=['POST'])
def restore_user(userId):
    user = User.query.filter_by(userId=userId, is_archived=True).first_or_404()

    try:
        user.is_archived = False
        db.session.commit()
        return jsonify({'message': 'User restored successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error restoring user: {e}'}), 500

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
