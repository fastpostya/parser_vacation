import os
import unittest
from utils.no_vac_error import NoVacationError
from utils.hh import HH
from utils.superjob import Superjob


class Test_HH_SJ(unittest.TestCase):
    def setUp(self):
        self.path = os.sep.join(["tests", "test_files", "test_open.json"])

    def test_hh(self) -> None:
        """ testing class HH"""
        hh = HH()
        list_vacation = hh.get_request("Java", 113, 1, 2)
        self.assertNotEqual(len(list_vacation), 0)
        with self.assertRaises(NoVacationError):
            list_vacation = hh.get_request("Java", 113, -1, 2)
        connector = hh.get_connector(self.path)
        self.assertEqual(connector.text, '{"key1":"value1"}')

    def test_sj(self) -> None:
        """ testing class Superjob"""
        hh = Superjob()
        list_vacation = hh.get_request("Java", 113, 1, 2)
        self.assertNotEqual(len(list_vacation), 0)
        with self.assertRaises(NoVacationError):
            list_vacation = hh.get_request("Java", 113, -1, 2)
        connector = hh.get_connector(self.path)
        self.assertEqual(connector.text, '{"key1":"value1"}')
