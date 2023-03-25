import os
import unittest
from utils.func import get_vacations_from_file


class Test_func(unittest.TestCase):
    """class for testing functions from module func"""
    def setUp(self):
        self.path = os.sep.join(
            [
                "tests",
                "test_files",
                "get_vacations_from_file.json"
                ]
        )
        self.path_one = os.sep.join(
            [
                "tests",
                "test_files",
                "get_vacations_from_file_one.json"
                ]
        )

    def test_get_vacations_from_file(self) -> list:

        # connector = Connector(self.path)
        new_list = get_vacations_from_file(self.path)
        self.assertEqual(len(new_list), 5)
        self.assertIsInstance(new_list, list)
        new_list_one = get_vacations_from_file(self.path_one)
        self.assertEqual(
            new_list_one[0].title,
            "Junior Python Backend Developer")
