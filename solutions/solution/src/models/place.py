import uuid
from datetime import datetime
from flask import current_app
from solutions.solution.src.persistence.dbinit import db
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship

class Place(db.Model):
    """Place class that links to the SQLite table places"""
    __tablename__ = 'places'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    address = db.Column(db.String(256), nullable=False)
    number_rooms = db.Column(db.Integer, nullable=False, default=0)
    number_bathrooms = db.Column(db.Integer, nullable=False, default=0)
    max_guest = db.Column(db.Integer, nullable=False, default=0)
    price_by_night = db.Column(db.Integer, nullable=False, default=0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    city_id = db.Column(db.String(36), db.ForeignKey('cities.id'), nullable=False)
    host_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    amenities = relationship("Amenity", secondary='place_amenity', back_populates="places")
    place_reviews = relationship("Review", back_populates="place", lazy=True, cascade="all, delete-orphan")
    city = relationship("City", back_populates="places", overlaps="city_info")

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Place {self.id} ({self.name} {self.created_at} {self.updated_at})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "number_rooms": self.number_rooms,
            "number_bathrooms": self.number_bathrooms,
            "max_guest": self.max_guest,
            "price_by_night": self.price_by_night,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city_id": self.city_id,
            "host_id": self.host_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(data: dict) -> "Place":
        """Create a new place"""
        repo = current_app.repository
        places = repo.get_all(Place)

        for p in places:
            if p.name == data["name"] and p.city_id == data["city_id"]:
                raise ValueError("Place already exists")
            
        new_place = Place(
            id=str(uuid.uuid4()),
            name=data["name"],
            description=data.get("description", ""),
            address=data.get("address", ""),
            number_rooms=data.get("number_rooms", 0),
            number_bathrooms=data.get("number_bathrooms", 0),
            max_guest=data.get("max_guest", 0),
            price_by_night=data.get("price_by_night", 0),
            latitude=data.get("latitude", None),
            longitude=data.get("longitude", None),
            city_id=data["city_id"],
            host_id=data["host_id"],
            created_at=datetime.utcnow(),  # Manually set created_at
            updated_at=datetime.utcnow()  # Manually set updated_at
        )
        repo.save(new_place)
        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place | None":
        """Update an existing place"""
        repo = current_app.repository
        place = repo.get(Place, place_id)
        if not place:
            return None
        if "name" in data:
            place.name = data["name"]
        if "description" in data:
            place.description = data["description"]
        if "address" in data:
            place.address = data["address"]
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
        if "host_id" in data:
            place.host_id = data["host_id"]
        place.updated_at = datetime.utcnow()  # Update updated_at manually
        repo.update(place)
        return place

    @staticmethod
    def delete(place_id: str) -> bool:
        """Delete a place"""
        repo = current_app.repository
        place = repo.get(Place, place_id)
        if not place:
            return False
        repo.delete(place)
        return True

    @staticmethod
    def get_all() -> list:
        """Get all places"""
        repo = current_app.repository
        return repo.get_all(Place)

    @staticmethod
    def get(place_id: str) -> "Place | None":
        """Get a place by ID"""
        repo = current_app.repository
        return repo.get(Place, place_id)
    
    @staticmethod
    def get_by_city(city_id: str) -> list:
        """Get all places in a city"""
        repo = current_app.repository
        return repo.get_by(Place, city_id=city_id)
    
    @staticmethod
    def get_by_host(host_id: str) -> list:
        """Get all places by a host"""
        repo = current_app.repository
        return repo.get_by(Place, user_id=host_id)
