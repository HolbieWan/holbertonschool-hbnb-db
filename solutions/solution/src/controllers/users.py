# solutions/solution/src/controllers/users.py

from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from solutions.solution.src.models.user import User
from solutions.solution.src.models.review import Review
from solutions.solution.src.models.place import Place

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    """Returns all users"""
    users = User.get_all()
    return jsonify([user.to_dict() for user in users])


@users_bp.route('/', methods=['POST'])
def create_user():
    """Creates a new user"""
    data = request.get_json()
    try:
        user = User.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))
    if user is None:
        abort(400, "User already exists")
    return jsonify(user.to_dict()), 201


@users_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    """Returns a user by ID"""
    user = User.get(user_id)
    if not user:
        abort(404, f"User with ID {user_id} not found")
    return jsonify(user.to_dict()), 200


@users_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Updates a user by ID"""
    data = request.get_json()
    try:
        user = User.update(user_id, data)
    except ValueError as e:
        abort(400, str(e))
    if user is None:
        abort(404, f"User with ID {user_id} not found")
    return jsonify(user.to_dict()), 200


@users_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Deletes a user by ID"""
    if not User.delete(user_id):
        abort(404, f"User with ID {user_id} not found")
    return '', 204


@users_bp.route('/<user_id>/places', methods=['GET'])
@jwt_required()
def get_places_from_user(user_id):
    """Returns all places from a specific user"""
    places = Place.get_all()
    return [place.to_dict() for place in places if place.host_id == user_id], 200


@users_bp.route('/<user_id>/reviews', methods=['GET'])
@jwt_required()
def get_reviews_from_user(user_id: str):
    """Returns all reviews from a specific user"""
    reviews = Review.get_all()
    return [review.to_dict() for review in reviews if review.user_id == user_id], 200


@users_bp.route('/admin_only', methods=['GET'])
@jwt_required()
def admin_only():
    user_id = get_jwt_identity()
    user = User.get(user_id)
    if not user.is_admin:
        abort(403, "Admin access required")
    return jsonify({"msg": "Welcome, admin!"}), 200
