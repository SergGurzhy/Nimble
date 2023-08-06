import json
import unittest
from db_factory import get_database
from model import Person


class TestDB(unittest.TestCase):

    db = get_database()
    initial_state_db = [
         {'first_name': 'Oleg', 'last_name': 'Mishyn', 'email': 'mystylename@gmail.com'},
         {'first_name': 'Ken', 'last_name': 'Underwood III', 'email': 'kenneth.underwood@yahoofinance.com'},
         {'first_name': 'kitty', 'last_name': 'akbar', 'email': 'asd1@gmail.com'}
    ]

    def test_update_success_new_value(self):
        with open('test_1.json', "r") as json_file:
            test_data = json.load(json_file)

        self.db.update_db(new_value=test_data)

        added_entries = [
            {'first_name': 'Jon', 'last_name': 'Ferrara', 'email': 'care@nimble.com'},
            {'first_name': 'James', 'last_name': 'McGillmore', 'email': 'jmcgillmore@heriks.com'},
        ]
        self.initial_state_db.extend(added_entries)

        result = self.db.get_all_records()
        expected_result = [Person(**rec) for rec in self.initial_state_db]

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
