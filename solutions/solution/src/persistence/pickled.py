"""
This module exports a Repository that persists data in a pickle file
"""

import pickle
from src.persistence.repository import Repository
from utils.constants import PICKLE_STORAGE_FILENAME


class PickleRepository(Repository):
    """Pickle Repository"""

    __filename = PICKLE_STORAGE_FILENAME
    __data: dict[str, list] = {
        "country": [],
        "user": [],
        "amenity": [],
        "city": [],
        "review": [],
        "place": [],
        "placeamenity": [],
    }

    def __init__(self) -> None:
        """Calls reload method"""
        self.reload()

    def _save_to_file(self):
        """Helper method to save the current object data to the file"""
        with open(self.__filename, "wb") as file:
            pickle.dump(self.__data, file)

    def get_all(self, model_name: str) -> list:
        """Get all objects of a given model"""
        return self.__data[model_name]

    def get(self, model_name: str, obj_id: str):
        """Get an object by its ID"""
        for obj in self.__data[model_name]:
            if obj.id == obj_id:
                return obj
        return None

    def reload(self):
        """Reloads the data from the pickle file"""
        try:
            with open(self.__filename, "rb") as file:
                self.__data = pickle.load(file)
        except FileNotFoundError:
            from src.models.country import Country

            self.__data["country"] = [Country("Uruguay", "UY")]
            self._save_to_file()

    def save(self, obj, save_to_file=True):
        """Save an object"""
        self.__data[obj.__class__.__name__.lower()].append(obj)
        if save_to_file:
            self._save_to_file()

    def update(self, obj):
        """Update an object"""
        for i, o in enumerate(self.__data[obj.__class__.__name__.lower()]):
            if o.id == obj.id:
                self.__data[obj.__class__.__name__.lower()][i] = obj
                self._save_to_file()
                return

    def delete(self, obj) -> bool:
        """Delete an object"""
        for i, o in enumerate(self.__data[obj.__class__.__name__.lower()]):
            if o.id == obj.id:
                del self.__data[obj.__class__.__name__.lower()][i]
                break

        self._save_to_file()
        return True
