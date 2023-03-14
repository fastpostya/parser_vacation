import json
import requests
from utils.no_vac_error import NoVacationError
from utils.engine_classes import Engine
from config import super_job_key
from utils.vacancy import Vacancy


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

    def get_request(self, keywords: str = "", town: str = "", \
            page: int = 1, count: int = 5) -> None:
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
        # здесь передается ключ доступа
        my_auth_data = {'X-Api-App-Id': self.superjob_key}   
    #    здесь передаются параметры запроса
        params={"keywords": self.keywords,
                                        "town": self.town,
                                        "page": self.page, 
                                        "count": self.count}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', \
            headers=my_auth_data, params=params)

        if response.status_code:        
            vacancies = json.loads(response.text)['objects']
            if len(vacancies):
                for vacancy in vacancies:
                    if "id" in vacancy:
                        # без id новый объект Vacancy не создаем
                        new_vacancy = Vacancy(vacancy["id"])
                        if "profession" in vacancy:
                            new_vacancy.title = vacancy["profession"]
                        if "payment_from" in vacancy:
                            new_vacancy.salary_from = vacancy["payment_from"]
                        if "payment_to" in vacancy:
                            new_vacancy.salary_to = vacancy["payment_to"]
                        if "currency" in vacancy:
                            new_vacancy.currency = vacancy["currency"]
                        if "vacancyRichText" in vacancy:
                            new_vacancy.description = vacancy["vacancyRichText"]
                        if ("client" in vacancy) and ("url" in vacancy):
                            new_vacancy.url = vacancy["client"]["url"]
                        if "firm_name" in vacancy:
                            new_vacancy.firm_name = vacancy["firm_name"]
                        self.elements.append(new_vacancy)

                # print(vacancy["id"], vacancy["profession"], vacancy["payment_from"], \
                # vacancy["payment_to"], vacancy["currency"],\
                # vacancy["candidat"], vacancy["vacancyRichText"], \
                # vacancy["firm_name"], vacancy["firm_activity"], \
                # vacancy["client"]["description"], vacancy["client"]["url"], \
                # vacancy["link"], vacancy["address"],\
                # vacancy["town"]["title"], vacancy["phones"], vacancy["firm_name"], \
                # vacancy["firm_activity"], vacancy["age_from"], vacancy["age_to"], vacancy["gender"])    
            else:
                raise NoVacationError(f"Вакансий с заданными параметрами не найдено:\n\
keywords={keywords}, town={town}, page={page}, count={count}")
        else:
            raise ConnectionError(response, response.text)

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass

    def print_info(self) -> None:
        """Печатает атрибут elements Superjob"""
        for i in self.elements:
            print(i)
