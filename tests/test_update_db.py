import unittest
from model import Person
from tests.base_test_case import BaseTestCase


class TestDB(BaseTestCase):

    def test_update_success_new_value(self):
        self.add_new_entry_with_json(file_name='test_1.json')
        added_entries = [
            {'first_name': 'Jon', 'last_name': 'Ferrara', 'email': 'care@nimble.com'},
            {'first_name': 'James', 'last_name': 'McGillmore', 'email': 'jmcgillmore@heriks.com'},
        ]
        self.initial_state_db.extend(added_entries)

        result = self.db.get_all_records()
        expected_result = [Person(**rec) for rec in self.initial_state_db]

        self.assertEqual(result, expected_result)

    def test_update_success_new_value_without_email(self):

        self.add_new_entry_with_json(file_name='test_2.json')
        added_entries = [
            {'first_name': 'Jon', 'last_name': 'Ferrara', 'email': 'care@nimble.com'},
            {'first_name': 'James', 'last_name': 'McGillmore', 'email': None},
        ]
        self.initial_state_db.extend(added_entries)

        result = self.db.get_all_records()
        expected_result = [Person(**rec) for rec in self.initial_state_db]

        self.assertEqual(result, expected_result)

    def test_try_update_exist_value(self):
        self.add_new_entry_with_json(file_name='test_3.json')
        added_entries = [
            {'first_name': 'Jon', 'last_name': 'Ferrara', 'email': 'care@nimble.com'},
        ]
        self.initial_state_db.extend(added_entries)

        result = self.db.get_all_records()
        expected_result = [Person(**rec) for rec in self.initial_state_db]

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
