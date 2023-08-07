import json
import unittest
from tests.database_test_case import DatabaseTestCase


class TestUpdateDB(DatabaseTestCase):

    """
    These test class should test the functionality of the database 'update_db' method.

       When each test is initialized, a mock database is created
       and filled with data from the 'file test_contacts.csv'.
    """

    def test_update_success_new_db(self):
        # Populate an empty database

        result = self.db.get_all_records()
        expected_result = json.dumps(self.initial_state_mock_db)
        self.assertEqual(expected_result, result)

    def test_update_success_new_value(self):

        self.update_db_with_json(file_name='test_data/test_1.json')
        last_id = self.count_elements_json_string(self.db.get_all_records())
        # Data to be added
        added_entries = [
            {'person_id': str(last_id - 1), 'first_name': 'Jon', 'last_name': 'Ferrara', 'email': 'care@nimble.com'},
            {'person_id': str(last_id), 'first_name': 'James', 'last_name': 'McGillmore', 'email': 'jmcgillmore@heriks.com'},
        ]
        self.initial_state_mock_db.extend(added_entries)

        result = self.db.get_all_records()
        expected_result = json.dumps(self.initial_state_mock_db)

        self.assertEqual(expected_result, result)

    def test_update_success_new_value_without_email(self):

        self.update_db_with_json(file_name='test_data/test_2.json')
        last_id = self.count_elements_json_string(self.db.get_all_records())

        # Data to be added
        added_entries = [
            {'person_id': str(last_id - 1), 'first_name': 'Jon', 'last_name': 'Ferrara', 'email': 'care@nimble.com'},
            {'person_id': str(last_id), 'first_name': 'James', 'last_name': 'McGillmore', 'email': None},
        ]
        self.initial_state_mock_db.extend(added_entries)

        result = self.db.get_all_records()
        expected_result = json.dumps(self.initial_state_mock_db)

        self.assertEqual(expected_result, result)

    def test_try_update_exist_email(self):
        # We are trying to add data in which the email already exists in the database.
        # Positive test: No data added

        self.update_db_with_json(file_name='test_data/test_3_email_exist.json')
        last_id = self.count_elements_json_string(self.db.get_all_records())
        # Data to be added
        added_entries = [
            {'person_id': str(last_id), 'first_name': 'Jon', 'last_name': 'Ferrara', 'email': 'care@nimble.com'},
        ]
        self.initial_state_mock_db.extend(added_entries)

        result = self.db.get_all_records()
        expected_result = json.dumps(self.initial_state_mock_db)

        self.assertEqual(expected_result, result)

    def test_try_update_exist_first_last_name_without_email(self):
        # We are trying to add data without email, in which the first and last names that are in the database.
        # Positive test: The name and surname of the record remain, and the mail field is deleted and becomes None

        self.update_db_with_json(file_name='test_data/test_4_oleg_exist.json')
        last_id = self.count_elements_json_string(self.db.get_all_records())
        # Data to be added
        id_rec = self.get_id_entry(email=self.initial_state_mock_db[0]['email'])
        added_entries = [
            {'person_id': str(last_id), 'first_name': 'Jon', 'last_name': 'Ferrara', 'email': 'care@nimble.com'},
        ]
        self.initial_state_mock_db.extend(added_entries)
        # update entry
        self.initial_state_mock_db[0] = {'person_id': id_rec, 'first_name': 'Oleg', 'last_name': 'Mishyn', 'email': None}

        result = self.db.get_all_records()
        expected_result = json.dumps(self.initial_state_mock_db)

        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
