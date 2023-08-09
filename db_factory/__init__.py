import os

from database.db_mock import MockDB
from database.db_sql import NimbleDbSQL
from db_factory.nimble_db import NimbleDB


def get_database() -> NimbleDB:
    env_kind = os.environ["DATABASE"].lower().strip()
    match env_kind:
        case "sql":
            return NimbleDbSQL()
        case "mock":
            return MockDB()

    raise RuntimeError(f"Unknown Database: {env_kind}")
