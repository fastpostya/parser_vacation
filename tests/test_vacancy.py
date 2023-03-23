import unittest
from utils.vacancy import Vacancy


class Test_Vacancy(unittest.TestCase):
    def setUp(self) -> None:
        self.vacancy = Vacancy("385678", "title", 1500.0, 150000.00, "url", "description", "RUB", "Very good firm", "HH")

    def test_str(self) -> None:
        self.assertEqual(str(self.vacancy),
                        ' id:385678, title, 1500.0 - 150000.0 Very good firm, HH')

        # f'{self.service} id:{self.id}, {self.title}, {self.salary_from} - {self.salary_to} {self.currency}, {self.firm_name}'

    def test_repr(self) -> None:
        self.assertEqual(repr(self.vacancy),
                        ' id:385678, title, 1500.0 - 150000.0 Very good firm, HH')