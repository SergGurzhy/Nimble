from abc import abstractmethod, ABC


class NimbleDB(ABC):

    @abstractmethod
    def create_table(self) -> None:
        """
        Create DB with fields:
                id serial PRIMARY KEY,
                email: varchar(50) PRIMARY KEY
                first_name: varchar(50)
                last_name:  varchar(50)
        """
        pass

    @abstractmethod
    def initialization_db(self, table_name: str):
        pass

    @abstractmethod
    def delete_table(self) -> None:
        pass

    @abstractmethod
    def update_db_from_csv_file(self) -> None:
        pass

    @abstractmethod
    def update_db(self, new_values: dict) -> None:
        """Updates the database with new received data."""
        pass

    @abstractmethod
    def fulltext_search(self, query: str) -> str:
        """
        :param query: str
        :return: json
        """
        pass

    @abstractmethod
    def get_all_entries(self) -> str:
        """
        :return: json
        """
        pass
