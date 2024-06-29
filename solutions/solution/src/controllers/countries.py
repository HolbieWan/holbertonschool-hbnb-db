"""
Countries controller module
"""

from flask import abort, Blueprint
from solutions.solution.src.models.city import City
from solutions.solution.src.models.country import Country
from flask import request


country_bp = Blueprint('countries', __name__)

@country_bp.route('/', methods=['POST'])
def create_country():
    """Creates a new country"""
    data = request.get_json()
    try:
        country = Country.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))
    return country.to_dict(), 201


@country_bp.route('/', methods=['GET'])
def get_countries():
    """Returns all countries"""
    countries: list[Country] = Country.get_all()
    return [country.to_dict() for country in countries]


@country_bp.route('/<code>', methods=['GET'])
def get_country_by_code(code: str):
    """Returns a country by code"""
    country: Country | None = Country.get_by_code(code)
    if not country:
        abort(404, f"Country with ID {code} not found")
    return country.to_dict()


@country_bp.route('/<code>/cities', methods=['GET'])
def get_country_cities(code: str):
    """Returns all cities for a specific country by code"""
    country: Country | None = Country.get_by_code(code)
    if not country:
        abort(404, f"Country with ID {code} not found")
    cities: list[City] = City.get_all()
    country_cities = [
        city.to_dict() for city in cities if city.country_code == country.code
    ]
    return country_cities

@country_bp.route('/<country_id>', methods=['PUT'])
def update_country(country_id: str):
    """Updates a country by ID"""
    data = request.get_json()
    updated_country: Country | None = Country.update(country_id, data)
    if not updated_country:
        abort(404, f"Country with ID {country_id} not found")
    return updated_country.to_dict()


@country_bp.route('/<country_id>', methods=['DELETE'])
def delete_country(country_id: str):
    """Deletes a country by ID"""
    if not Country.delete(country_id):
        abort(404, f"Country with ID {country_id} not found")
    return "", 204




