from abc import abstractmethod, ABC
from model import Person


class NimbleDB(ABC):

    @abstractmethod
    def create_table(self) -> None:
        """
        Create DB with fields:
                email: varchar(50) PRIMARY KEY
                first_name: varchar(50)
                last_name:  varchar(50)
        """
        pass

    @abstractmethod
    def delete_table(self, table_name: str) -> None:
        pass

    @abstractmethod
    def update_db_from_csv_file(self, file_name: str) -> None:
        pass

    @abstractmethod
    def update_db(self, new_value: dict) -> None:  # , new_value: dict
        """Updates the database with new received data."""
        pass

    @abstractmethod
    def fulltext_search(self, query: str) -> list[Person]:
        pass

    @abstractmethod
    def get_all_records(self) -> list[Person]:
        pass