import uuid
from datetime import datetime
from flask import current_app
from solutions.solution.src.persistence.dbinit import db
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Review(db.Model):
    """Review representation"""

    __tablename__ = "reviews"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    comment = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    place = relationship("Place", back_populates="place_reviews", lazy=True)
    user = relationship("User", back_populates="reviews", lazy=True)

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Review {self.id} - '{self.comment[:25]}...'>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(data: dict) -> "Review":
        """Create a new review"""
        repo = current_app.repository
        new_review = Review(
            id=str(uuid.uuid4()),  # Ensure ID is set correctly
            place_id=data["place_id"],
            user_id=data["user_id"],
            comment=data["comment"],
            rating=data["rating"],
            created_at=datetime.utcnow(),  # Set created_at manually
            updated_at=datetime.utcnow()  # Set updated_at manually
        )
        repo.save(new_review)
        return new_review

    @staticmethod
    def update(review_id: str, data: dict) -> "Review | None":
        """Update an existing review"""
        repo = current_app.repository
        review = repo.get(Review, review_id)
        if not review:
            return None
        if "comment" in data:
            review.comment = data["comment"]
        if "rating" in data:
            review.rating = data["rating"]
        review.updated_at = datetime.utcnow()  # Update updated_at manually
        repo.update(review)
        return review

    @staticmethod
    def delete(review_id: str) -> bool:
        """Delete a review"""
        repo = current_app.repository
        review = repo.get(Review, review_id)
        if not review:
            return False
        repo.delete(review)
        return True

    @staticmethod
    def get_all() -> list:
        """Get all reviews"""
        repo = current_app.repository
        return repo.get_all(Review)

    @staticmethod
    def get(review_id: str) -> "Review | None":
        """Get a review by ID"""
        repo = current_app.repository
        return repo.get(Review, review_id)
