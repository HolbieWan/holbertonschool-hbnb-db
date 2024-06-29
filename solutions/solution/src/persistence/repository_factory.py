# solutions/solution/src/persistence/repository_factory.py

from solutions.solution.src.persistence.dbinit import db
from solutions.solution.src.persistence.memory import MemoryRepository
from solutions.solution.src.persistence.db import DBRepository

def get_repository(storage_type='db'):
    if storage_type == 'memory':
        return MemoryRepository()
    elif storage_type == 'db':
        return DBRepository()
    else:
        raise ValueError(f"Unknown storage type: {storage_type}")
