class NoVacationError(Exception):
    """Класс NoVacationError для обработки исключения, возникающего
    в случае, если в запросе к сайту с вакансиями не вернется ни одной.
    Атрибуты:
    -message:str - сообщение об ошибке

    Методы:
    -__init__-инициализация класса
    -__str__- возвращает строку для печати с сообщением об ошибке
    """
    def __init__(self, message=""):
        if message:
            self.message = message
        else:
            self.message = None

    def __str__(self):
        """возвращает тип ошибки и сообщение"""
        return "NoVacationError: " + str(self.message)
      
