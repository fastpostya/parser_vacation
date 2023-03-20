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

    # @classmethod
    # def get_superjob_key(cls) -> None:
    #     """Метод класса записывает в переменную класса superjob_key
    #     значение ключа для доступа к сайту superjob из переменной
    #     super_job_key, которая находится в файле config.py"""
    #     cls.superjob_key = super_job_key

    def get_request(self, keywords: str = "", area: int =113,\
            page: int = 1, per_page: int = 50) -> None:
        """Метод отправляет GET- запрос к сайту и возвращает данные
        в формате JSON.
        Атрибуты:
        - keywords: str - ключевое слово для поиска вакансии
        - town: str|i- название города для поиска или его ID
        - area
        - page: int -Номер страницы результата поиска
        - per_page: int - Количество результатов на страницу поиска.


integer
Количество элементов на странице выдачи. Поддерживаются стандартные параметры пагинации. Значение по умолчанию и максимальное значение per_page составляет 10000

page
integer
Порядковый номер страницы в выдаче. Поддерживаются стандартные параметры пагинации. По умолчанию нумерация начинается с 0 страницы

        """
        self.keywords = keywords
        # self.town = town
        self.page = page
        self.count = per_page
        self.area = area


        # здесь передаются параметры запроса
        params = {'per_page': self.count,
                    'text': self.keywords,
                    'page':self.page,
                    'per_page': self.count,
                    'User-Agent': 'MyApp/1.0 (something@useful.com)',
                    'area': self.area}
        # per_page=10&page=199 (выдача с 1991 по 2000 вакансию)
        # 'area': "113" - регион Россия
#         1 - Москва
        # 1202 -Новосибирск

        url = "https://api.hh.ru/vacancies"
        response = requests.get(url, params=params)

        if response.status_code:
            text_json = json.loads(response.text)
            if "bad_argument" in text_json:
                raise NoVacationError(f"Ошибочный ответ {text_json}")
            else:
                vacancies = text_json["items"]
                if len(vacancies):
                    return vacancies
                    # for vacancy in vacancies:
                    #     if "id" in vacancy:
                    #         # без id новый объект HHVacancy не создаем
                    #         new_vacancy = HHVacancy(vacancy["id"])
                    #         if "name" in vacancy:
                    #             new_vacancy.title = vacancy["name"]
                    #         if vacancy["salary"] and ("salary" in vacancy) and ("from" in vacancy["salary"]):
                    #             new_vacancy.salary_from = vacancy["salary"]["from"]
                    #         if vacancy["salary"] and ("salary" in vacancy) and ("to" in vacancy["salary"]):
                    #             new_vacancy.salary_to = vacancy["salary"]["to"]
                    #         if vacancy["salary"] and ("salary" in vacancy) and ("currency" in vacancy["salary"]):
                    #             new_vacancy.currency = vacancy["salary"]["currency"]
                    #         if "requirement" in vacancy:
                    #             new_vacancy.description = vacancy["requirement"]
                    #         if "url" in vacancy:
                    #             new_vacancy.url = vacancy["url"]
                    #         if ("employer" in vacancy) and ("name" in vacancy["employer"]):
                    #             new_vacancy.firm_name = vacancy["employer"]["name"]
                    #         self.elements.append(new_vacancy)

                            # vacancy["requirement"],
                            # vacancy["response_url"],
                            # vacancy["apply_alternate_url"],
                            # vacancy["url"],
                            # vacancy["employer"]["name"],
                            # vacancy["snippet"]["requirement"],
                            # vacancy["snippet"]["responsibility"]
                else:
                    raise NoVacationError(f"Вакансий с заданными параметрами не найдено:\n\
keywords={keywords}, page={page}, per_page={per_page}, area={self.area}")
        else:
            raise ConnectionError(response, response.text)

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        connector = Connector(file_name)
        return connector

    # def print_info(self) -> None:
    #     """Печатает атрибут elements HHVacancy"""
    #     for i in self.elements:
    #         print(i)
