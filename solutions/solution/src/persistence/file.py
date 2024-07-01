"""
This module exports a Repository that persists data in a JSON file
"""
import uuid
from datetime import datetime
import json
from solutions.solution.src.models.base import Base
from solutions.solution.src.persistence.repository import Repository
from solutions.solution.utils.constants import FILE_STORAGE_FILENAME

from solutions.solution.src.models.amenity import Amenity, PlaceAmenity
from solutions.solution.src.models.city import City
from solutions.solution.src.models.country import Country
from solutions.solution.src.models.place import Place
from solutions.solution.src.models.review import Review
from solutions.solution.src.models.user import User


class FileRepository(Repository):
    """File Repository"""

    __filename = FILE_STORAGE_FILENAME
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
        serialized = {
            k: [v.to_dict() for v in l if type(v) is not dict]
            for k, l in self.__data.items()
        }
        #print(f"Saving data to {self.__filename}: {json.dumps(serialized, indent=2)}")
        with open(self.__filename, "w") as file:
            json.dump(serialized, file, indent=2)

    def _get_model_name(self, model_name):
        """Helper method to ensure model_name is a string"""
        if isinstance(model_name, type):
            return model_name.__name__.lower()
        return model_name.lower()

    def get_all(self, model_name: str):
        """Get all objects of a given model"""
        model_name_str = self._get_model_name(model_name)
        return self.__data.get(model_name_str, [])

    def get(self, model_name: str, obj_id: str):
        """Get an object by its ID"""
        model_name_str = self._get_model_name(model_name)
        for obj in self.get_all(model_name_str):
            if obj.id == obj_id:
                return obj
        return None

    def get_by_code(self, model_name: str, code: str):
        """Get an object by its code (only applicable for Country in this context)"""
        model_name_str = self._get_model_name(model_name)
        for obj in self.get_all(model_name_str):
            if getattr(obj, "code", None) == code:
                return obj
        return None

    def reload(self):
        """Reloads the data from the file"""
        file_data = {}
        try:
            with open(self.__filename, "r") as file:
                file_data = json.load(file)
            #print(f"Loaded data from {self.__filename}: {json.dumps(file_data, indent=2)}")
        except FileNotFoundError:
            print(f"File {self.__filename} not found. Initializing default data.")
            self._initialize_default_data()
            self._save_to_file()
            return  # No need to load data after initializing default

        self._load_data(file_data)

    def _initialize_default_data(self):
        """Initialize default data if file not found"""
        print("Initializing default data")
        default_country = Country(
            id=str(uuid.uuid4()), 
            name="Uruguay", 
            code="UY", 
            created_at=datetime.utcnow(), 
            updated_at=datetime.utcnow()
        )
        self.__data["country"] = [default_country]

    def _load_data(self, file_data):
        """Load data from file into the repository"""
        models = {
            "amenity": Amenity,
            "city": City,
            "country": Country,
            "place": Place,
            "placeamenity": PlaceAmenity,
            "review": Review,
            "user": User,
        }
        for model_name, data_list in file_data.items():
            for item in data_list:
                instance = self._instantiate_model(models[model_name], item)
                if instance:
                    self.save(data=instance, save_to_file=False)

    def _instantiate_model(self, model_class, data):
        """Instantiate a model dynamically"""
        instance = model_class(**data)
        if "created_at" in data:
            instance.created_at = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data:
            instance.updated_at = datetime.fromisoformat(data["updated_at"])
        return instance

    def save(self, data: Base, save_to_file=True):
        """Save an object to the repository"""
        model: str = data.__class__.__name__.lower()

        if model not in self.__data:
            self.__data[model] = []

        self.__data[model].append(data)
        #print(f"Saved object to model {model}: {data.to_dict()}")

        if save_to_file:
            self._save_to_file()

    def update(self, obj: Base):
        """Update an object in the repository"""
        cls = obj.__class__.__name__.lower()

        for i, o in enumerate(self.__data[cls]):
            if o.id == obj.id:
                obj.updated_at = datetime.now()
                self.__data[cls][i] = obj
                self._save_to_file()
                return obj

        return None

    def delete(self, obj: Base):
        """Delete an object from the repository"""
        class_name = obj.__class__.__name__.lower()

        if obj not in self.__data[class_name]:
            return False

        self.__data[class_name].remove(obj)

        self._save_to_file()

        return True
