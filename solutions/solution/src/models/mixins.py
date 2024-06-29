# src/models/mixins.py
from abc import abstractmethod
from typing import Any

class BaseMixin:
    @abstractmethod
    def to_dict(self) -> dict:
        """Returns the dictionary representation of the object"""
        pass

    @staticmethod
    @abstractmethod
    def create(data: dict) -> Any:
        """Creates a new object of the class"""
        pass

    @staticmethod
    @abstractmethod
    def update(entity_id: str, data: dict) -> Any:
        """Updates an object of the class"""
        pass
