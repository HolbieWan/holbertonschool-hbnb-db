"""
City related functionality
"""
import uuid
from datetime import datetime
from solutions.solution.src.persistence.dbinit import db
from solutions.solution.src.models.base import Base
from solutions.solution.src.models.country import Country
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class City(db.Model):
    """City class that links to the SQLite table cities"""
    __tablename__ = 'cities'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    country_code = db.Column(db.String(36), db.ForeignKey('countries.code'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    city_places = relationship("Place", back_populates="city", lazy=True, overlaps="city_info")


    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<City {self.id} ({self.name} {self.created_at} {self.updated_at})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(city: dict) -> "City":
        """Create a new city"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        cities = City.query.all()
        for c in cities:
            if c.name == city["name"]:
                raise ValueError("City already exists")
        new_city = City(
            name=city["name"],
            country_code=city["country_code"]
        )
        repo = get_repository()
        repo.save(new_city)
        return new_city


    @staticmethod
    def update(city_id: str, data: dict) -> "City | None":
        """Update an existing city"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        city = City.query.get(city_id)
        if not city:
            return None
        if "name" in data:
            city.name = data["name"]
        if "country_code" in data:
            city.country_code = data["country_code"]
        repo = get_repository()
        repo.update(city)
        return city


    @staticmethod
    def delete(city_id: str) -> bool:
        """Delete a city"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        city = City.query.get(city_id)
        if not city:
            return False
        repo = get_repository()
        repo.delete(city)
        return True


    @staticmethod
    def get_all() -> list:
        """Get all cities"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        repo = get_repository()
        return repo.get_all(City)


    @staticmethod
    def get(city_id: str) -> "City | None":
        """Get a city by ID"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        repo = get_repository()
        return repo.get(City, city_id)
