import json

from db_factory import get_database
from tests.base_test_case import BaseTestCase


class DatabaseTestCase(BaseTestCase):

    db = get_database()

    def setUp(self) -> None:
        self.initial_state_mock_db = [
            {
                'person_id': '1',
                'first_name': 'Oleg',
                'last_name': 'Mishyn',
                'email': 'mystylenameg@gmail.com',
                'description': 'Seasoned B2B.'
            },
            {
                'person_id': '2',
                'first_name': 'Ken',
                'last_name': 'Underwood III',
                'email': 'kenneth.underwood@yahoofinance.com',
                'description': 'Accomplished business development.'
            },
            {
                'person_id': '3',
                'first_name': 'kitty',
                'last_name': 'akbar', ''
                'email': None,
                'description': 'Dynamic sales.'
            }
        ]
        self.db.create_table(table_name='storage')
        self.db.initialization_db('storage')

    def tearDown(self) -> None:
        self.db.delete_table(table_name='storage')
        del self.initial_state_mock_db

    def get_id_entry(self, email: str) -> str | None:
        result = [rec['person_id'] for rec in self.initial_state_mock_db if rec.get('email') == email]
        return result[0]

    def update_db_with_json(self, file_name: str) -> None:
        with open(file_name, "r") as json_file:
            test_data = json.load(json_file)
        self.db.update_db(new_values=test_data)