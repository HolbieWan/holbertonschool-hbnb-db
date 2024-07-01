import os
import pytest
from flask import Flask
from config import config
from solutions.solution.src.persistence.dbinit import db  # Assurez-vous que c'est un objet SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Importer les modèles
from solutions.solution.src.models.user import User
from solutions.solution.src.models.review import Review
from solutions.solution.src.models.place import Place
from solutions.solution.src.models.amenity import Amenity, PlaceAmenity
from solutions.solution.src.models.country import Country
from solutions.solution.src.models.city import City

# Configurer la base de données de test
basedir = os.path.abspath(os.path.dirname(__file__))
TEST_DB = 'test.db'

@pytest.fixture(scope='module')
def app():
    app = Flask(__name__)
    app.config.from_object(config['development'])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='module')
def db_instance(app):
    return db

def test_create_user(db_instance):
    user = User(email="test@example.com", first_name="John", last_name="Doe", password="password123")
    db_instance.session.add(user)
    db_instance.session.commit()
    assert user.id is not None

def test_create_place(db_instance):
    place = Place(
        name="Test Place",
        description="A place for testing",
        number_rooms=1,
        number_bathrooms=1,
        max_guest=2,
        price_by_night=100,
        city_id="some-city-id",
        host_id="some-host-id"
    )
    db_instance.session.add(place)
    db_instance.session.commit()
    assert place.id is not None

def test_create_review(db_instance):
    review = Review(
        place_id="some-place-id",
        user_id="some-user-id",
        comment="Great place!",
        rating=5
    )
    db_instance.session.add(review)
    db_instance.session.commit()
    assert review.id is not None

def test_create_country(db_instance):
    country = Country(name="Test Country", code="TC")
    db_instance.session.add(country)
    db_instance.session.commit()
    assert country.id is not None

def test_create_city(db_instance):
    city = City(name="Test City", country_code="TC")
    db_instance.session.add(city)
    db_instance.session.commit()
    assert city.id is not None

def test_create_amenity(db_instance):
    amenity = Amenity(name="WiFi")
    db_instance.session.add(amenity)
    db_instance.session.commit()
    assert amenity.id is not None

def test_place_amenity_association(db_instance):
    place_amenity = PlaceAmenity(place_id="some-place-id", amenity_id="some-amenity-id")
    db_instance.session.add(place_amenity)
    db_instance.session.commit()
    assert place_amenity.place_id is not None and place_amenity.amenity_id is not None
