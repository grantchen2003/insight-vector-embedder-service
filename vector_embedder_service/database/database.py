from typing import Optional

from .base_database import BaseDatabase
from .chroma_db import ChromaDb


singleton_instance: Optional[BaseDatabase] = None


def get_singleton_instance() -> BaseDatabase:
    global singleton_instance
    if singleton_instance is None:
        singleton_instance = ChromaDb()

    return singleton_instance