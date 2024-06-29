# solutions/solution/src/models/country.py

import uuid
from datetime import datetime
from solutions.solution.src.persistence.dbinit import db
from solutions.solution.src.models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime


class Country(db.Model):
    """Country class that links to the SQLite table countries"""
    __tablename__ = 'countries'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(2), nullable=False)  # Adding the code attribute
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cities = relationship('City', backref='country', lazy=True)


    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Country {self.id} ({self.name} {self.code} {self.created_at} {self.updated_at})>"


    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


    @staticmethod
    def create(country: dict) -> "Country":
        """Create a new country"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        new_country = Country(
            name=country["name"],
            code=country["code"]
        )
        repo = get_repository()
        repo.save(new_country)
        return new_country


    @staticmethod
    def update(country_id: str, data: dict) -> "Country | None":
        """Update an existing country"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        country = Country.query.get(country_id)
        if not country:
            return None
        if "name" in data:
            country.name = data["name"]
        if "code" in data:
            country.code = data["code"]
        repo = get_repository()
        repo.update(country)
        return country


    @staticmethod
    def delete(country_id: str) -> bool:
        """Delete a country"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        country = Country.query.get(country_id)
        if not country:
            return False
        repo = get_repository()
        repo.delete(country)
        return True


    @staticmethod
    def get_all() -> list:
        """Get all countries"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        repo = get_repository()
        return repo.get_all(Country)


    @staticmethod
    def get(country_id: str) -> "Country | None":
        """Get a country by ID"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        repo = get_repository()
        return repo.get(Country, country_id)
    
    @staticmethod
    def get_by_code(code: str) -> "Country | None":
        """Get a country by code"""
        from solutions.solution.src.persistence.repository_factory import get_repository
        repo = get_repository()
        return repo.get_by_code(Country, code)
