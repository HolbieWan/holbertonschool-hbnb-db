import os

if os.getenv('USE_DATABASE') == 'True':
    from solutions.solution.src.persistence.db import DatabaseStorage as Storage
else:
    from solutions.solution.src.persistence.file import FileStorage as Storage