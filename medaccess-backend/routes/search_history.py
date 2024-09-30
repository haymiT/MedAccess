from flask import Blueprint, request, jsonify
from models import db, SearchHistory

search_history_bp = Blueprint('search_history', __name__)

@search_history_bp.route('/', methods=['POST'])
def add_search():
    data = request.get_json()
    new_search = SearchHistory(
        userID=data['userID'],
        medicationID=data['medicationID'],
        resultCount=data['resultCount']
    )
    db.session.add(new_search)
    db.session.commit()
    return jsonify({"message": "Search history recorded successfully"}), 201
