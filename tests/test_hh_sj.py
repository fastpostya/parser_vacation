import os
import unittest
from utils.no_vac_error import NoVacationError
from utils.hh import HH
from utils.superjob import Superjob


class Test_HH_SJ(unittest.TestCase):
    def setUp(self):
        self.path = os.sep.join(["tests", "test_files", "test_open.json"])

    def test_hh_find(self) -> None:
        """ testing class HH. Vacancy finded."""
        hh = HH()
        # 113 -Russia
        list_vacation = hh.get_request("Java", 113, 1, 2)
        self.assertNotEqual(len(list_vacation), 0)
        # 1 -Moscow
        list_vacation = hh.get_request("Java", 1, 1, 2)
        self.assertNotEqual(len(list_vacation), 0)

    def test_hh_no_find(self) -> None:
        """ Testing class HH. Vacancy did not find."""
        hh = HH()
        with self.assertRaises(NoVacationError):
            text = hh.get_request("Java", "smth", -1, 2)
            print(text)
        connector = hh.get_connector(self.path)
        self.assertEqual(connector.text, '{"key1":"value1"}')

    def test_sj_find(self) -> None:
        """ testing class Superjob. Vacancy finded."""
        sj = Superjob()
        list_vacation = sj.get_request("Python", "Москва", 1, 2)
        self.assertNotEqual(len(list_vacation), 0)

    def test_sj_no_find(self) -> None:
        """ Testing class Superjob. Vacancy did not find."""
        sj = Superjob()
        with self.assertRaises(NoVacationError):
            sj.get_request("суперкрутой", "Тверь", 1, 2)
        connector = sj.get_connector(self.path)
        self.assertEqual(connector.text, '{"key1":"value1"}')
