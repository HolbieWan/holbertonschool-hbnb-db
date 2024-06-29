""" Populate the database with some data at the start of the application"""

from src.persistence.repository import Repository


def populate_db(repo: Repository) -> None:
    """Populates the db with a dummy country"""
    from src.models.country import Country

    countries = [
        Country(name="Uruguay", code="UY"),
    ]

    for country in countries:
        repo.save(country)

    print("Memory DB populated")
