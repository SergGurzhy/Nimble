import json
import sys
import unittest
from dotenv import load_dotenv


class BaseTestCase(unittest.TestCase):

    load_dotenv(sys.path[0] + '/env_test.env')

    def count_elements_json_string(self, json_string: str):
        """
        This method is needed to get the number of mock database records.
        :param json_string: json string
        :return: count of main elements json string
        """
        return len(json.loads(json_string))

    @staticmethod
    def get_test_json(file_name: str) -> str:
        """

        :return: json
        """
        with open(file_name, "r") as json_file:
            data = json.load(json_file)
        return data
