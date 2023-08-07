from model import Person
from db_factory.nimble_db import NimbleDB


class DB:
    def __init__(self, database: NimbleDB):
        self.database = database

    def create_db(self) -> None:
        self.database.create_table()

    def delete_table(self, table_name: str) -> None:
        self.database.delete_table(table_name=table_name)

    def update_db_from_csv_file(self, file_name: str) -> None:
        self.database.update_db_from_csv_file(file_name=file_name)

    def update_db(self, new_value: dict) -> None:
        """Updates the database with new received data."""
        self.database.update_db(new_value=new_value)

    def fulltext_search(self, query: str) -> str:
        return self.database.fulltext_search(query=query)

    def get_all_records(self) -> str:
        return self.database.get_all_records()
