import sys

from dotenv import load_dotenv

from db_factory import NimbleDB

load_dotenv(sys.path[0] + '/env_test.env')


class ServiceDB:

    def __init__(self, db: NimbleDB) -> None:
        self.db = db

    def drop_table(self, table_name: str) -> None:
        self.db.delete_table(table_name)

    def initialisation_db(self, table_name: str) -> None:
        self.db.initialization_db(table_name=table_name)

    def get_all_entries(self) -> str:
        return self.db.get_all_entries()

    def full_text_search(self, query: str) -> str:
        return self.db.fulltext_search(query)

    def update_db(self, new_values: dict) -> dict[str]:
        return self.db.update_db(new_values)
