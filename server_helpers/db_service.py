from db_factory import NimbleDB


class ServiceDB:

    def __init__(self, db: NimbleDB) -> None:
        self.db = db

    def start_project(self, file_name: str) -> None:
        self.db.create_table()
        self.db.update_db_from_csv_file(file_name=file_name)

    def drop_table(self, table_name: str) -> None:
        self.db.delete_table(table_name=table_name)

    def get_all_entries(self) -> str:
        return self.db.get_all_records()

