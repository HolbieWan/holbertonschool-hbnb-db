import uuid
from datetime import datetime
from typing import Any, Optional
from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, DateTime, ForeignKey
from solutions.solution.src.models.mixins import BaseMixin
from solutions.solution.src.persistence.dbinit import db

db = SQLAlchemy()

class Base(BaseMixin, db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(
        self,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        if id is None:
            self.id = str(uuid.uuid4())
        if created_at is None:
            self.created_at = datetime.utcnow()
        if updated_at is None:
            self.updated_at = datetime.utcnow()

    @classmethod
    def get(cls, id: str) -> Optional["Any"]:
        from src.persistence.repository_factory import get_repository
        repo = get_repository()
        return repo.get(cls, id)

    @classmethod
    def get_all(cls) -> list["Any"]:
        from src.persistence.repository_factory import get_repository
        repo = get_repository()
        return repo.get_all(cls)

    @classmethod
    def delete(cls, id: str) -> bool:
        from src.persistence.repository_factory import get_repository
        repo = get_repository()
        obj = cls.get(id)
        if not obj:
            return False
        return repo.delete(obj)