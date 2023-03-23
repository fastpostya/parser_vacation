import json
import requests
from utils.no_vac_error import NoVacationError
from utils.engine_classes import Engine
from config import super_job_key
from utils.connector import Connector


class Superjob(Engine):
    """Class Superjob for working with superjob.ru.
    Class atribute:
    - superjob_key: str- the key for acsess for superjob
    """
    superjob_key = ""
    # elements = []

    def __init__(self) -> None:
        """Инициализация объекта класса Superjob"""
        self.get_superjob_key()

    @classmethod
    def get_superjob_key(cls) -> None:
        """The classmethod writes to a variable of the superjob_key class
    the value of the key for accessing the superjob.ru site from
    the super_job_key variable, which is located in the file config.py
        """
        cls.superjob_key = super_job_key

    def get_request(self, keywords: str = "", town: str = "",
                    page: int = 0, count: int = 100) -> None:
        """The method sends a GET request to the site and returns data
        in JSON format.

        Attributes:
        - keywords: str - keyword for job search
        - town: str|i- the name of the city to search for or its ID
        - page: int - page number of the search result
        - count: int - the number of results per search page.
        The maximum number of results is 100.
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
            raise NoVacationError(f"Вакансий с заданными\
 параметрами не найдено:\n\
keywords={keywords}, town={town}, page={page}, count={count}")


    @staticmethod
    def get_connector(file_name: str) -> Connector:
        """ Возвращает экземпляр класса Connector """
        connector = Connector(file_name)
        return connector
