import json
import requests
from utils.no_vac_error import NoVacationError
from utils.engine_classes import Engine
from utils.connector import Connector
# from utils.vacancy import Vacancy, HHVacancy


class HH(Engine):
    """Класс HH для работы с сайтом hh.ru.
    """
    elements = []

    def __init__(self) -> None:
        """Инициализация объекта класса HH"""
        pass

    def get_request(self, keywords: str = "",
                    area: int =113,
                    per_page: int = 100,
                    page: int = 0,) -> None:
        """Метод отправляет GET- запрос к сайту и возвращает данные
        в формате JSON.
        Атрибуты:
        - keywords: str - ключевое слово для поиска вакансии
        - area: str|i-название города для поиска или его ID
            (113 - регион Россия, 1 - Москва, 1202 -Новосибирск)
        - page: int -Номер страницы результата поиска
        - per_page: int - Количество результатов на страницу поиска.
        """
        self.keywords = keywords
        # self.town = town
        self.count = per_page
        self.page = page
        self.area = area
        list_vacations = []
        is_response_successful = False
        for i in range(5):
            self.page = i

            # здесь передаются параметры запроса
            params = {'per_page': self.count,
                        'text': self.keywords,
                        'per_page': self.count,
                        'page':self.page,
                        'User-Agent': 'MyApp/1.0 (something@useful.com)',
                        'area': self.area}

            url = "https://api.hh.ru/vacancies"
            response = requests.get(url, params=params)

            if response.status_code:
                is_response_successful = True
                text_json = json.loads(response.text)
                if "bad_argument" in text_json:
                    raise NoVacationError(f"Ошибочный ответ {text_json}")
                else:
                    vacancies = text_json["items"]
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
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        connector = Connector(file_name)
        return connector

    # def print_info(self) -> None:
    #     """Печатает атрибут elements HHVacancy"""
    #     for i in self.elements:
    #         print(i)
