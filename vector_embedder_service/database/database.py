from typing import Optional

from .base_database import BaseDatabase
from .postgresql import PostgreSql


singleton_instance: Optional[BaseDatabase] = None


def get_singleton_instance() -> BaseDatabase:
    global singleton_instance
    if singleton_instance is None:
        singleton_instance = PostgreSql()

    return singleton_instance