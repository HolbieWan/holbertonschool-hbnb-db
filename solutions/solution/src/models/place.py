"""
Place related functionality
"""

import uuid
from datetime import datetime
from solutions.solution.src.persistence.dbinit import db
from solutions.solution.src.models.base import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Integer, Table
from sqlalchemy.orm import relationship, Mapped


class Place(db.Model):
    """Place class that links to the SQLite table places"""
    __tablename__ = 'places'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    number_rooms = db.Column(db.Integer, nullable=False, default=0)
    number_bathrooms = db.Column(db.Integer, nullable=False, default=0)
    max_guest = db.Column(db.Integer, nullable=False, default=0)
    price_by_night = db.Column(db.Integer, nullable=False, default=0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    city_id = db.Column(db.String(36), db.ForeignKey('cities.id'), nullable=False)
    host_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    amenities = relationship("Amenity", secondary='place_amenity', back_populates="places")
    users = relationship("User", backref="hosted_places", lazy=True)
    place_reviews = relationship("Review", back_populates="place", lazy=True, cascade="all, delete-orphan", overlaps="place_reviews")
    city = relationship("City", back_populates="city_places", overlaps="city_info")
    

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Place {self.id} ({self.name} {self.created_at} {self.updated_at})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "number_rooms": self.number_rooms,
            "number_bathrooms": self.number_bathrooms,
            "max_guest": self.max_guest,
            "price_by_night": self.price_by_night,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city_id": self.city_id,
            "host_id": self.host_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(place: dict) -> "Place":
        """Create a new place"""
        from solutions.solution.src.persistence.repository_factory import get_repository

        new_place = Place(
            name=place["name"],
            description=place.get("description", ""),
            number_rooms=place.get("number_rooms", 0),
            number_bathrooms=place.get("number_bathrooms", 0),
            max_guest=place.get("max_guest", 0),
            price_by_night=place.get("price_by_night", 0),
            latitude=place.get("latitude", None),
            longitude=place.get("longitude", None),
            city_id=place["city_id"],
            host_id=place["host_id"]
        )
        repo = get_repository()
        repo.save(new_place)
        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place | None":
        """Update an existing place"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        place = Place.query.get(place_id)
        if not place:
            return None
        if "name" in data:
            place.name = data["name"]
        if "description" in data:
            place.description = data["description"]
        if "number_rooms" in data:
            place.number_rooms = data["number_rooms"]
        if "number_bathrooms" in data:
            place.number_bathrooms = data["number_bathrooms"]
        if "max_guest" in data:
            place.max_guest = data["max_guest"]
        if "price_by_night" in data:
            place.price_by_night = data["price_by_night"]
        if "latitude" in data:
            place.latitude = data["latitude"]
        if "longitude" in data:
            place.longitude = data["longitude"]
        if "city_id" in data:
            place.city_id = data["city_id"]
        if "user_id" in data:
            place.host_id = data["host_id"]
        repo = get_repository()
        repo.update(place)
        return place

    @staticmethod
    def delete(place_id: str) -> bool:
        """Delete a place"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        place = Place.query.get(place_id)
        if not place:
            return False
        repo = get_repository()
        repo.delete(place)
        return True


    @staticmethod
    def get_all() -> list:
        """Get all places"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        repo = get_repository()
        return repo.get_all(Place)


    @staticmethod
    def get(place_id: str) -> "Place | None":
        """Get a place by ID"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        repo = get_repository()
        return repo.get(Place, place_id)
