"""
Reviews controller module
"""

from flask import abort, request, Blueprint
from solutions.solution.src.models.review import Review


reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/', methods=['GET'])
def get_reviews():
    """Returns all reviews"""
    reviews = Review.get_all()
    return [review.to_dict() for review in reviews], 200


@reviews_bp.route('/<place_id>/review', methods=['POST'])
def create_review(place_id: str):
    """Creates a new review"""
    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing field: user_id")
    if "place_id" not in data:
        abort(400, "Missing field: place_id")
    try:
        review = Review.create(data | {"place_id": place_id})
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))
    return review.to_dict(), 201


@reviews_bp.route('/<place_id>/reviews', methods=['GET'])
def get_reviews_from_place(place_id: str):
    """Returns all reviews from a specific place"""
    reviews = Review.get_all()
    return [
        review.to_dict() for review in reviews if review.place_id == place_id
    ], 200


@reviews_bp.route('/<user_id>/reviews', methods=['GET'])
def get_reviews_from_user(user_id: str):
    """Returns all reviews from a specific user"""
    reviews = Review.get_all()
    return [
        review.to_dict() for review in reviews if review.user_id == user_id
    ], 200


@reviews_bp.route('/<review_id>', methods=['GET'])
def get_review_by_id(review_id: str):
    """Returns a review by ID"""
    review: Review | None = Review.get(review_id)
    print(f"Review ID: {review_id}")
    print(f"Review: {review}")
    if not review:
        abort(404, f"Review with ID {review_id} not found")
    return review.to_dict(), 200


@reviews_bp.route('/<review_id>', methods=['PUT'])
def update_review(review_id: str):
    """Updates a review by ID"""
    data = request.get_json()
    try:
        review: Review | None = Review.update(review_id, data)
    except ValueError as e:
        abort(400, str(e))
    if not review:
        abort(404, f"Review with ID {review_id} not found")
    return review.to_dict(), 200


@reviews_bp.route('/<review_id>', methods=['DELETE'])
def delete_review(review_id: str):
    """Deletes a review by ID"""
    if not Review.delete(review_id):
        abort(404, f"Review with ID {review_id} not found")
    return "", 204
