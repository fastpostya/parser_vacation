# Парсер вакансий

Проект __Парсер вакансий__ создан для работы с API двух сайтов - hh.ru и superjob.ru.
Для работы с ними реализованы несколько классов.

## Класс Connector
__Класс Connector__ реализует доступ к файлу. Инициализируется строкой, содержащей путь к файлу. Файл должен содержать данные в json формате.

Methods:
*   is_valid_json: bool - cheking if file is in JSON-format.
*   is_file_exist: bool -cheking if file exists
*   read_file: str - getting text from file data_file
*   is_file_not_old: bool - checking if file not older than number days
*   save_date: str - saving data in file data_file
*   insert: dict | list - insert data in file with saving it's structure.
*   select: list | KeyError - selecting dates from file.
        The key is the field for filtering. The value is the desired value.
*   delete: list | KeyError - deleting date, using query.

    Atributes:

*   data_file:str - the path to the json-file. It has getter and setter.
*   text: str - the text from the file
*   save_date: list - list for saving in file
*   delete_query: dict - dict for deleting data
*   select_query: dict - dict for selection data
*   days_outdate: int - the number of days after which the file
    is outdated

## Класс Vacancy
__Класс Vacancy__ представляет объект для работы с вакансией.

Atributes:

*   id:int -  id of the vacancy on the source site,
*   title:str - job title,
*   salary_from: float - minimum salary level,
*   salary_to: float - maximum salary level,
*   url:str - vacancy address,
*   description:str -  job description,
*   firm_name:str -name of the employer organization,
*   service:str- the name of the site from which vacancies were received.
    Takes the values HH and SJ.

## Класс HH
__Класс HH__ создан для работы с сайтом hh.ru.

Methods:

*   get_request(self, keywords: str = "",
                    area: int = 113,
                    per_page: int = 100,
                    page: int = 0,) -> None: The method sends a GET request to the site and returns data
        in JSON format
*   get_connector(file_name: str) -> Connector:
        Returns the instance of class Connector

## Класс Superjob
__Класс Superjob__ создан для работы с сайтом superjob.ru.

Class atribute:
*   superjob_key: str- the key for acsess for superjob

Methods:

*   \_\_init__(self) -> None: - Intialisation the instance of class Superjob

*   get_superjob_key(cls) -> None - The classmethod writes to a variable of the superjob_key class the value of the key for accessing the superjob.ru site from the super_job_key variable, which is located in the file config.py


*   get_request(self, keywords: str = "", town: str = "",
                    page: int = 0, count: int = 100) -> None:
        The method sends a GET request to the site and returns data
        in JSON format.

## Класс NoVacationError
__Класс NoVacationError__ создан для обработки исключения, которое выбрасывается в случае, если при запросе к сайту с вакансиями ни одно не найдено.



## Функции
*   sorting(vacancies: list) -> list: сортирует список объектов Vacancy по зарплате
*   get_top(vacancies: list, top_count: int) -> list: возвращает топ-10 вакансий с самой высокой зарплатой
*   get_vacations_from_file(file_path: str): возвращает список вакансий из файла

## Работа с программой

Ключевое слово (keyword) и путь к файлу (file_path) с данными для поиска вакансии задаются в файле config.py.
При запуске появляется меню

    ------Парсер вакансий------
    Выберите нужное действие:
    1 - Сделать запрос на сайт superjob.ru и сохранить данные в файл
    2 - Сделать запрос на сайт hh.ru и сохранить данные в файл
    3 - Получить данные из файла
    4 - Удалить вакансии от заданной организации (только для superjob)
    5 - Выход.

При выборе пунктов 1 и 2 данные с сайтов superjob.ru и hh.ru будут добавлены файл. Будет выдан запрос на очистку файла перед записью. Для подтверждения нужно нажать 'y'.
Если файл устарел (создан более, чем 1 день назад) будет предложено обновить запрос.

При выборе пункта 3 появится меню

    Выберите нужное действие:
    1 - Напечатать количество вакансий в файле
    2 - Напечатать вакансии
    3 - Отсортировать вакансии по зарплате.
    4 - Вывести 10 вакансий с наивысшей оплатой.

При выборе 1 будет напечатано количество вакансий в файле.
2 - будут выведены все вакансии из файла,
3 - они будут отсортированы по зарплате и выведены на экран,
4 - будут выведены 10 вакансий с наивысшей оплатой.

При выборе 4 в главном меню появится возможность удалить вакансии, содержащие название организации, которое пользователь введет с клавиатуры.
