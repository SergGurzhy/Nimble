import os

from database.db_moke import MokeDB
from database.db_sql import NimbleDbSQL
from db_factory.nimble_db import NimbleDB


def get_database() -> NimbleDB:
    env_kind = os.environ["DATABASE"].lower()
    match env_kind:
        case "sql":
            return NimbleDbSQL()
        case "moke":
            return MokeDB()

    raise RuntimeError(f"Unknown Database: {env_kind}")
