import unittest
from utils.no_vac_error import NoVacationError


class Test_NoVacationError(unittest.TestCase):

    def test_no_vac_raise(self) -> None:
        with self.assertRaises(NoVacationError):
            raise NoVacationError()
        with self.assertRaises(NoVacationError):
            raise NoVacationError("Текст сообщения")
        self.assertEqual(str(NoVacationError("текст")),
                        "NoVacationError: текст")
