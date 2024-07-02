import uuid
from datetime import datetime
from flask import current_app
from solutions.solution.src.persistence.dbinit import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey

class Country(db.Model):
    """Country class that links to the SQLite table countries"""
    __tablename__ = 'countries'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(2), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cities = relationship('City', back_populates='country', lazy=True, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Country {self.id} ({self.name} {self.code} {self.created_at} {self.updated_at})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(country: dict) -> "Country":
        """Create a new country"""
        repo = current_app.repository

        # Check if the country already exists
        existing_country = repo.get_by_code(Country, code=country["code"])
        if existing_country:
            raise ValueError(f"Country with code {country['code']} already exists")

        new_country = Country(
            id=str(uuid.uuid4()),
            name=country["name"],
            code=country["code"],
            created_at=datetime.utcnow(),  # Manually set created_at
            updated_at=datetime.utcnow()  # Manually set updated_at
        )
        repo.save(new_country)
        return new_country

    @staticmethod
    def update(country_id: str, data: dict) -> "Country | None":
        """Update an existing country"""
        repo = current_app.repository
        country = repo.get(Country, country_id)
        if not country:
            return None
        # Check if the updated code already exists for another country
        if "code" in data:
            existing_country = repo.get_by_code(Country, code=data["code"])
            if existing_country and existing_country.id != country_id:
                raise ValueError(f"Country with code {data['code']} already exists")
        if "name" in data:
            country.name = data["name"]
        if "code" in data:
            country.code = data["code"]
        country.updated_at = datetime.utcnow()  # Update updated_at manually
        repo.update(country)
        return country

    @staticmethod
    def delete(country_id: str) -> bool:
        """Delete a country"""
        repo = current_app.repository
        country = repo.get(Country, country_id)
        if not country:
            return False
        repo.delete(country)
        return True

    @staticmethod
    def get_all() -> list:
        """Get all countries"""
        repo = current_app.repository
        return repo.get_all(Country)

    @staticmethod
    def get(country_id: str) -> "Country | None":
        """Get a country by ID"""
        repo = current_app.repository
        return repo.get(Country, country_id)
    
    @staticmethod
    def get_by_code(code: str) -> "Country | None":
        """Get a country by code"""
        repo = current_app.repository
        return repo.get_by_code(Country, code)
