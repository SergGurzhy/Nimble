from db_factory import NimbleDB


class ServiceDB:

    def __init__(self, db: NimbleDB) -> None:
        self.db = db

    def drop_table(self) -> None:
        self.db.delete_table()

    def get_all_entries(self) -> str:
        return self.db.get_all_records()

    def full_text_search(self, query: str) -> str:
        return self.db.fulltext_search(query)

    def update_db(self, new_values: dict) -> None:
        self.db.update_db(new_values)
