""" This module is responsible for selecting the repository
to be used based on the environment variable REPOSITORY_ENV_VAR."""

import os

from solutions.solution.src.persistence.repository import Repository
from solutions.solution.utils.constants import REPOSITORY_ENV_VAR

repo: Repository

if os.getenv(key=REPOSITORY_ENV_VAR) == "db":
    from solutions.solution.src.persistence.db import DBRepository

    repo = DBRepository()
elif os.getenv(REPOSITORY_ENV_VAR) == "file":
    from solutions.solution.src.persistence.file import FileRepository

    repo = FileRepository()
elif os.getenv(REPOSITORY_ENV_VAR) == "pickle":
    from solutions.solution.src.persistence.pickled import PickleRepository

    repo = PickleRepository()
else:
    from solutions.solution.src.persistence.memory import MemoryRepository

    repo = MemoryRepository()

print(f"Using {repo.__class__.__name__} as repository")
