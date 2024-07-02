import uuid
from datetime import datetime
from flask import current_app
from solutions.solution.src.persistence.dbinit import db
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class City(db.Model):
    """City class that links to the SQLite table cities"""
    __tablename__ = 'cities'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    country_code = db.Column(db.String(2), db.ForeignKey('countries.code'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    country = relationship('Country', back_populates='cities', lazy=True)
    places = relationship("Place", back_populates="city", lazy=True, cascade="all, delete-orphan", overlaps="city_info")

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<City {self.id} ({self.name} {self.created_at} {self.updated_at})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(city: dict) -> "City":
        """Create a new city"""
        repo = current_app.repository
        cities = repo.get_all(City)
        for c in cities:
            if c.name == city["name"] and c.country_code == city["country_code"]:
                raise ValueError("City already exists")
        new_city = City(
            id=str(uuid.uuid4()),
            name=city["name"],
            country_code=city["country_code"],
            created_at=datetime.utcnow(),  # Manually set created_at
            updated_at=datetime.utcnow()  # Manually set updated_at
        )
        repo.save(new_city)
        return new_city

    @staticmethod
    def update(city_id: str, data: dict) -> "City | None":
        """Update an existing city"""
        repo = current_app.repository
        city = repo.get(City, city_id)
        if not city:
            return None
        if "name" in data:
            city.name = data["name"]
        if "country_code" in data:
            city.country_code = data["country_code"]
        city.updated_at = datetime.utcnow()  # Update updated_at manually
        repo.update(city)
        return city

    @staticmethod
    def delete(city_id: str) -> bool:
        """Delete a city"""
        repo = current_app.repository
        city = repo.get(City, city_id)
        if not city:
            return False
        repo.delete(city)
        return True

    @staticmethod
    def get_all() -> list:
        """Get all cities"""
        repo = current_app.repository
        return repo.get_all(City)

    @staticmethod
    def get(city_id: str) -> "City | None":
        """Get a city by ID"""
        repo = current_app.repository
        return repo.get(City, city_id)
    
    @staticmethod
    def get_by_country(country_code: str) -> list:
        """Get all cities by country code"""
        repo = current_app.repository
        return repo.get_by(City, "country_code", country_code)
