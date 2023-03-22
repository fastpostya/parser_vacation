import json
import requests
from utils.no_vac_error import NoVacationError
from utils.engine_classes import Engine
from config import super_job_key
from utils.vacancy import SJVacancy
from utils.connector import Connector


class Superjob(Engine):
    """Класс Superjob для работы с сайтом superjob.
    Атрибут класса:
    - superjob_key: str- ключ для доступа к сайту superjob
    """
    superjob_key = ""
    elements = []

    def __init__(self) -> None:
        """Инициализация объекта класса Superjob"""
        # self.keywords = ""
        self.get_superjob_key()

    @classmethod
    def get_superjob_key(cls) -> None:
        """Метод класса записывает в переменную класса superjob_key
        значение ключа для доступа к сайту superjob из переменной
        super_job_key, которая находится в файле config.py"""
        cls.superjob_key = super_job_key

    def get_request(self, keywords: str = "", town: str = "",
                    page: int = 0, count: int = 100) -> None:
        """Метод отправляет GET- запрос к сайту и возвращает данные
        в формате JSON.
        Атрибуты:
        - keywords: str - ключевое слово для поиска вакансии
        - town: str|i- название города для поиска или его ID
        - page: int -Номер страницы результата поиска
        - count: int - Количество результатов на страницу поиска.
        Максимальное число результатов - 100.
        """
        self.keywords = keywords
        self.town = town
        self.page = page
        self.count = count
        list_vacations = []
        is_response_successful = False
        # здесь передается ключ доступа
        my_auth_data = {'X-Api-App-Id': self.superjob_key}
        for i in range(5):
            self.page = i
            # здесь передаются параметры запроса
            params = {"keywords": self.keywords,
                        "town": self.town,
                        "page": self.page,
                        "count": self.count}
            response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                    headers=my_auth_data,
                                    params=params)

            if response.status_code:
                is_response_successful = True
                vacancies = json.loads(response.text)['objects']
                if len(vacancies):
                    for vacancy in vacancies:
                        list_vacations.append(vacancy)
        if not is_response_successful:
            raise ConnectionError(response, response.text)
        if len(list_vacations):
            print(f"Добавлено {len(list_vacations)} вакансий")
            input("Для продолжения нажмите любую клавишу.")
            return list_vacations
        else:
            raise NoVacationError(f"Вакансий с заданными параметрами не найдено:\n\
keywords={keywords}, town={town}, page={page}, count={count}")


    @staticmethod
    def get_connector(file_name: str) -> Connector:
        """ Возвращает экземпляр класса Connector """
        connector = Connector(file_name)
        return connector

    # def print_info(self) -> None:
    #     """Печатает атрибут elements Superjob"""
    #     for i in self.elements:
    #         print(i)
