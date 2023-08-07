import json
import unittest
from db_factory import get_database


class BaseTestCase(unittest.TestCase):
    db = get_database()

    def update_db_with_json(self, file_name: str) -> None:
        with open(file_name, "r") as json_file:
            test_data = json.load(json_file)
        self.db.update_db(new_values=test_data)

    def count_elements_json_string(self, json_string: str):
        """
        This method is needed to get the number of mock database records.
        :param json_string: json string
        :return: count of main elements json string
        """
        return len(json.loads(json_string))

