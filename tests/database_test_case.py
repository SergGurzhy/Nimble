from tests.base_test_case import BaseTestCase


class DatabaseTestCase(BaseTestCase):

    def setUp(self) -> None:
        self.initial_state_mock_db = [
            {'person_id': '1', 'first_name': 'Oleg', 'last_name': 'Mishyn', 'email': 'mystylename@gmail.com'},
            {'person_id': '2', 'first_name': 'Ken', 'last_name': 'Underwood III',
             'email': 'kenneth.underwood@yahoofinance.com'},
            {'person_id': '3', 'first_name': 'kitty', 'last_name': 'akbar', 'email': None}
        ]
        self.db.create_table()
        self.db.update_db_from_csv_file(file_name='test_data/test_contacts.csv')

    def tearDown(self) -> None:
        self.db.delete_table(table_name='storage')
        del self.initial_state_mock_db

    def get_id_entry(self, email: str) -> str | None:
        result = [rec['person_id'] for rec in self.initial_state_mock_db if rec.get('email') == email]
        return result[0]
