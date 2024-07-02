import uuid
from datetime import datetime
from flask import current_app
from solutions.solution.src.persistence.dbinit import db
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Amenity(db.Model):
    """Amenity class that links to the SQLite table amenities"""
    __tablename__ = 'amenities'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    places = relationship("Place", secondary='place_amenity', back_populates="amenities")

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Amenity {self.id} ({self.name} {self.created_at} {self.updated_at})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(data: dict) -> "Amenity":
        """Create a new amenity"""
        repo = current_app.repository
        amenities = repo.get_all(Amenity)
        for amenity in amenities:
            if amenity.name == data["name"]:
                raise ValueError("Amenity already exists")
        new_amenity = Amenity(
            id=str(uuid.uuid4()),  # Ensure ID is set correctly
            name=data["name"],
            created_at=datetime.utcnow(),  # Set created_at manually
            updated_at=datetime.utcnow()  # Set updated_at manually
        )
        repo.save(new_amenity)
        return new_amenity

    @staticmethod
    def update(amenity_id: str, data: dict) -> "Amenity | None":
        """Update an existing amenity"""
        repo = current_app.repository
        amenity = repo.get(Amenity, amenity_id)
        if not amenity:
            return None
        if "name" in data:
            amenity.name = data["name"]
        amenity.updated_at = datetime.utcnow()  # Update updated_at manually
        repo.update(amenity)
        return amenity

    @staticmethod
    def delete(amenity_id: str) -> bool:
        """Delete an amenity"""
        repo = current_app.repository
        amenity = repo.get(Amenity, amenity_id)
        if not amenity:
            return False
        repo.delete(amenity)
        return True

    @staticmethod
    def get_all() -> list:
        """Get all amenities"""
        repo = current_app.repository
        return repo.get_all(Amenity)

    @staticmethod
    def get(amenity_id: str) -> "Amenity | None":
        """Get an amenity by ID"""
        repo = current_app.repository
        return repo.get(Amenity, amenity_id)


class PlaceAmenity(db.Model):
    """Association table for places and amenities"""
    __tablename__ = 'place_amenity'
    place_id = db.Column(db.String(36), ForeignKey('places.id'), primary_key=True)
    amenity_id = db.Column(db.String(36), ForeignKey('amenities.id'), primary_key=True)

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<PlaceAmenity (place_id={self.place_id}, amenity_id={self.amenity_id})>"