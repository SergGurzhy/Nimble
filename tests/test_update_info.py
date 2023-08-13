from tests.base_test_case import BaseTestCase
from db_factory import get_database
from server_helpers.db_service import ServiceDB
from unittest.mock import patch, MagicMock
from server_helpers.helpers import update_db_daily


class TestResponseNimbleAPI(BaseTestCase):

    db_service = ServiceDB(get_database())

    @patch('server_helpers.helpers.requests')
    def test_liquid_data(self, request_moke) -> None:

        request_response_moke = MagicMock()
        request_moke.get.return_value = request_response_moke
        request_response_moke.status_code = 200
        request_response_moke.json.return_value = self.get_test_json(file_name='test_data/test_1.json')
        actual_result = update_db_daily(self.db_service)
        expected_result = {'count_insert': '2', 'count_update': '0'}
        self.assertEqual(expected_result, actual_result)

    @patch('server_helpers.helpers.requests')
    def test_not_liquid_statuscode(self, request_moke) -> None:
        request_response_moke = MagicMock()
        request_moke.get.return_value = request_response_moke
        request_response_moke.status_code = 500
        request_response_moke.json.return_value = {
                                                     "message": "Internal error handling request",
                                                     "code": 107
                                                  }
        actual_result = update_db_daily(self.db_service)

        expected_result = {'ERROR': f'An error occurred connecting to the server. Status_code: 500'}
        self.assertEqual(expected_result, actual_result)

    # TODO  handle all Nimble endpoint errors

        ...
