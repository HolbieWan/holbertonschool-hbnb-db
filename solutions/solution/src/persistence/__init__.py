""" This module is responsible for selecting the repository
to be used based on the environment variable REPOSITORY_ENV_VAR."""

import os
from solutions.solution.src.persistence.repository import Repository
from solutions.solution.utils.constants import REPOSITORY_ENV_VAR

def get_repository() -> Repository:
    repo: Repository
    repo_env = os.getenv(REPOSITORY_ENV_VAR, 'memory')
    print(f"get_repository: REPOSITORY_ENV_VAR is set to: {repo_env}")

    if repo_env == "db":
        from solutions.solution.src.persistence.db import DBRepository
        repo = DBRepository()
        print("get_repository: Initialized DBRepository")
    elif repo_env == "file":
        from solutions.solution.src.persistence.file import FileRepository
        repo = FileRepository()
        print("get_repository: Initialized FileRepository")
    elif repo_env == "pickle":
        from solutions.solution.src.persistence.pickled import PickleRepository
        repo = PickleRepository()
        print("get_repository: Initialized PickleRepository")
    else:
        from solutions.solution.src.persistence.memory import MemoryRepository
        repo = MemoryRepository()
        print("get_repository: Initialized MemoryRepository")

    print(f"get_repository: Using {repo.__class__.__name__} as repository")
    return repo
