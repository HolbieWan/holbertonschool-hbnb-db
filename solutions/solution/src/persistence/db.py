# solutions/solution/src/persistence/db.py

from solutions.solution.src.models.base import Base
from solutions.solution.src.persistence.repository import Repository
from solutions.solution.src.persistence.dbinit import db

class DBRepository(Repository):
    def get_all(self, model) -> list:
        return model.query.all()

    def get(self, model, obj_id: str) -> db.Model | None:
        return model.query.get(obj_id)
    
    def get_by_code(self, model, code: str) -> db.Model | None:
        return model.query.filter_by(code=code).first()

    def save(self, obj: db.Model) -> None:
        db.session.add(obj)
        db.session.commit()

    def update(self, obj: db.Model) -> db.Model | None:
        db.session.commit()
        return obj

    def delete(self, obj: db.Model) -> bool:
        db.session.delete(obj)
        db.session.commit()
        return True

    def reload(self):
        db.session.rollback()
