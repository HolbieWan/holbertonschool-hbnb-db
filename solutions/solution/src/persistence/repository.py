# solutions/solution/src/persistence/repository.py

from abc import ABC, abstractmethod
from solutions.solution.src.persistence.dbinit import db
from solutions.solution.src.models.base import Base

class Repository(ABC):
    @abstractmethod
    def get_all(self, model) -> list:
        pass

    @abstractmethod
    def get(self, model, obj_id: str) -> db.Model | None:
        pass

    @abstractmethod
    def get_by_code(self, model, code: str) -> db.Model | None:
        pass
    
    @abstractmethod
    def save(self, obj: db.Model) -> None:
        pass

    @abstractmethod
    def update(self, obj: db.Model) -> db.Model | None:
        pass

    @abstractmethod
    def delete(self, obj: db.Model) -> bool:
        pass

    @abstractmethod
    def reload(self):
        pass
