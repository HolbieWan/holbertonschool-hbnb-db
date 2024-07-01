# solutions/solution/utils/populate.py

from solutions.solution.src.models.country import Country
from solutions.solution.src.models.city import City
from solutions.solution.src.models.user import User
from solutions.solution.src.models.place import Place
from solutions.solution.src.models.review import Review
from solutions.solution.src.models.amenity import Amenity

def populate_db(repo):
    repo.save(Country(name="Uruguay", code="UY"))
    repo.save(Country(name="Argentina", code="AR"))
    repo.save(Country(name="Brazil", code="BR"))
    repo.save(Country(name="Chile", code="CL"))

    repo.save(City(name="Montevideo", country_code="UY"))
    repo.save(City(name="Buenos Aires", country_code="AR"))
    repo.save(City(name="São Paulo", country_code="BR"))
    repo.save(City(name="Santiago", country_code="CL"))

    repo.save(User(email="user1@example.com", first_name="User", last_name="One", password="password1"))
    repo.save(User(email="user2@example.com", first_name="User", last_name="Two", password="password2"))

    repo.save(Place(name="Nice Place", city_id="some-city-id", host_id="some-user-id"))
    repo.save(Review(place_id="some-place-id", user_id="some-user-id", comment="Great place!", rating=5))
    repo.save(Amenity(name="Pool"))
