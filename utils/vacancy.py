class Vacancy:
    """Класс Vacancy для представления объекта вакансии.
    Атрибуты:
    - id:int - id вакансии на сайте-источнике,
    - title:str - название вакансии,
    - salary_from: float - минимальный уровень зарплаты,
    - salary_to: float - максимальный уровень зарплаты,
    - url:str - адрес вакансии,
    - description:str - описание вакансии
    - firm_name:str -название организации-работодателя
    - service:str- название сайта, с которого получены вакансии.
    Принимает значения HH и SJ
      """
    __slots__ = ('id', 'title', 'salary_from', 'salary_to', 'salary', 'url', \
        'description', 'currency', 'firm_name', 'service')

    def __init__(self, id, title: str = "", salary_from: float = 0.0,\
            salary_to: float = 0.0,
            salary: float = 0.0, url: str = "", description: str = "",\
            currency: str = "", firm_name: str = "", service: str = ""):
        self.id = id
        self.title = title
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary = salary
        self.currency = currency
        self.url = url
        self.description = description
        self.firm_name = firm_name
        self.service = service

    def __str__(self):
        return f'{self.service} id:{self.id}, {self.title}, {self.salary_from} - {self.salary_to} {self.currency}, {self.firm_name}'
# {self.url}\n{self.description})'

    def __repr__(self):
        return f'{self.service} id:{self.id}, {self.title}, {self.salary_from} - {self.salary_to} {self.currency}, {self.firm_name}'

# on future
# class CountMixin:

#     @property
#     def get_count_of_vacancy(self):
#         """
#         Вернуть количество вакансий от текущего сервиса.
#         Получать количество необходимо динамически из файла.
#         """
#         pass


class HHVacancy(Vacancy):  # add counter mixin
    """ HeadHunter Vacancy """
    def __init__(self, id, *kvargs):
        Vacancy.__init__(self, id, *kvargs)
        self.service = "HH"

    def __str__(self):
        return f'HH: {self.firm_name}, зарплата: {self.salary} руб/мес'


class SJVacancy(Vacancy):  # add counter mixin
    """ SuperJob Vacancy """
    def __init__(self, id, *kvargs):
        Vacancy.__init__(self, id, *kvargs)
        self.service = "SJ"

    def __str__(self):
        return f'SJ: {self.firm_name}, зарплата: {self.salary} руб/мес'