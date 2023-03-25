import unittest
from utils.jobs_classes import sorting, get_top
from utils.vacancy import Vacancy
from utils.no_vac_error import NoVacationError


class Test_job_classes(unittest.TestCase):

    def setUp(self) -> None:
        self.dict = [Vacancy("01", "первая", 0, 0, 100),
                    Vacancy("02", "вторая", 0, 0, 50),
                    Vacancy("03", "третья", 0, 0, 150),
                    Vacancy("04", "четвертая", 0, 0, 75)
        ]

        self.dict_11 = [Vacancy("01", "первая", 0, 0, 100),
                    Vacancy("02", "вторая", 0, 0, 50),
                    Vacancy("03", "третья", 0, 0, 150),
                    Vacancy("04", "четвертая", 0, 0, 75),
                    Vacancy("05", "пятая", 0, 0, 874),
                    Vacancy("06", "шестая", 0, 0, 365),
                    Vacancy("07", "седьмая", 0, 0, 250),
                    Vacancy("08", "восьмая", 0, 0, 750),
                    Vacancy("09", "девятая", 0, 0, 35),
                    Vacancy("10", "десятая", 0, 0, 1500),
                    Vacancy("11", "одиннадцатая", 0, 0, 250)
        ]
        self.empty_dict = []

    def test_sorting_empty(self) -> list | NoVacationError:
        with self.assertRaises(NoVacationError):
            sorting(self.empty_dict)

    def test_sorting_not_empty(self) -> list | NoVacationError:
        sorted_list = sorting(self.dict)
        self.assertEqual(sorted_list[0].salary, 150)
        self.assertEqual(sorted_list[1].salary, 100)
        self.assertEqual(sorted_list[2].salary, 75)

    def test_get_top_empty(self) -> list | NoVacationError:
        with self.assertRaises(NoVacationError):
            get_top(self.empty_dict, 3)

    def test_get_top_not_empty(self) -> list | NoVacationError:
        sorted_list = get_top(self.dict_11, 3)
        self.assertEqual(sorted_list[0].salary, 1500)
        self.assertEqual(sorted_list[1].salary, 874)
        self.assertEqual(sorted_list[2].salary, 750)

        sorted_list = get_top(self.dict_11, 10)
        self.assertEqual(len(sorted_list), 10)
