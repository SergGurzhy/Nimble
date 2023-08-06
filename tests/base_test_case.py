import json
import unittest

from db_factory import get_database


class BaseTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.db = get_database()
        self.initial_state_db = [
            {'first_name': 'Oleg', 'last_name': 'Mishyn', 'email': 'mystylename@gmail.com'},
            {'first_name': 'Ken', 'last_name': 'Underwood III', 'email': 'kenneth.underwood@yahoofinance.com'},
            {'first_name': 'kitty', 'last_name': 'akbar', 'email': 'asd1@gmail.com'}
        ]

    def tearDown(self) -> None:
        self.db.delete_table(table_name='storage')

    def add_new_entry_with_json(self, file_name: str) -> None:
        with open(file_name, "r") as json_file:
            test_data = json.load(json_file)

        self.db.update_db(new_value=test_data)

