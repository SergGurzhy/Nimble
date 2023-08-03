from abc import abstractmethod


class NimbleDB:

    @abstractmethod
    def create_db(self) -> None:
        """
        Create DB with fields:
                email: varchar(50) PRIMARY KEY
                first_name: varchar(50)
                last_name:  varchar(50)
        """
        pass

    @abstractmethod
    def update_db_from_csv_file(self, file_name: str) -> None:
        pass

    @abstractmethod
    def insert_value(self, values: tuple[str, str, str]) -> None:
        pass

    @abstractmethod
    def update_value(self, value: tuple[str, str], key: str) -> None:
        pass

    @abstractmethod
    def update_db(self) -> None:
        pass

