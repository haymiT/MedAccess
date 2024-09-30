from flask import Blueprint, request, jsonify
from models import db, User

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    new_user = User(
        userEmail=data['userEmail'],
        userPassword=data['userPassword'],
        userType=data['userType'],
        userPhoneNumber=data.get('userPhoneNumber')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(userEmail=data['userEmail']).first()
    if user and user.userPassword == data['userPassword']:
        return jsonify({"message": "Login successful", "userID": user.userID}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "userID": user.userID,
        "userEmail": user.userEmail,
        "userType": user.userType,
        "userPhoneNumber": user.userPhoneNumber
    })
