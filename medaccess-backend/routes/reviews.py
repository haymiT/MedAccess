from flask import Blueprint, request, jsonify
from models import db, Review

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/', methods=['POST'])
def add_review():
    data = request.get_json()
    new_review = Review(
        userID=data['userID'],
        pharmacyID=data['pharmacyID'],
        medicationID=data['medicationID'],
        rating=data['rating'],
        reviewText=data['reviewText']
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "Review added successfully", "reviewID": new_review.reviewID}), 201
