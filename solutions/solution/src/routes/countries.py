"""
This module contains the routes for the countries endpoint
"""

from flask import Blueprint
from src.controllers.countries import (
    get_countries,
    get_country_by_code,
    get_country_cities,
)

countries_bp = Blueprint("countries", __name__, url_prefix="/countries")

countries_bp.route("/", methods=["GET"])(get_countries)
countries_bp.route("/<code>", methods=["GET"])(get_country_by_code)
countries_bp.route("/<code>/cities", methods=["GET"])(get_country_cities)
