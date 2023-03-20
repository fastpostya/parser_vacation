from json import JSONDecodeError
import click
from config import super_job_key, keyword, file_path
from utils.superjob import Superjob
from utils.hh import HH
from utils.no_vac_error import NoVacationError
from utils.connector import Connector
from utils.vacancy import Vacancy

import pprint


def clrscr():
    # Clear screen using click.clear() function
    click.clear()


def get_from_sj(file_path: str):
    """Get request from superjob.ru and insert date in file 'file_path'"""
    print("Делаем запрос на сайт Superjob")
    clear = input("Очистить файл?\n y/n")

     # Создаем экземпляр класса Superjob для поиска вакансий на сайте superjob
    superjob = Superjob()
    try:
        answer = superjob.get_request(keyword, "Тверь")
    except ConnectionError as error:
        print(error)
    except NoVacationError as error:
        print(error)

    connector = superjob.get_connector(file_path)
    if clear == "y":
        connector.save_date("")

    try:
        connector.insert(answer)
    except KeyError as error:
        print(error)
    except JSONDecodeError as error:
        print(error)
    # with open(file_path, "r", encoding="utf-8") as file:
    #     print(file.read())
    # print(connector.text)


def get_from_hh(file_path: str):
    """Get request from superjob.ru and insert date in file 'file_path'"""
    print("Делаем запрос на сайт Superjob")
    clear = input("Очистить файл?\n y/n")
    # Создаем экземпляр класса HHVacancy
    hh = HH()
    try:
        answer = hh.get_request(keyword, "1202")
    except ConnectionError as error:
        print(error)
    except NoVacationError as error:
        print(error)
    connector_hh = hh.get_connector(file_path)
    if clear == "y":
        connector_hh.save_date("")
    try:
        connector_hh.insert(answer)
    except KeyError as error:
        print(error)
    except JSONDecodeError as error:
        print(error)
    # print(connector_hh.text)


def get_vacations_from_file(file_path: str):
    list_vacancies = []
    connector = Connector(file_path)
    vacancies = connector.read_file()
    if vacancies:
        for vacancy in vacancies:
            if "id" in vacancy:
                # без id новый объект Vacancy не создаем
                id = vacancy["id"]
                title = ""
                salary_from = ""
                salary_to = ""
                url = ""
                description = ""
                currency = ""
                firm_name = ""
                if "profession" in vacancy:
                    title = vacancy["profession"]
                    service = "SJ"
                    if "payment_from" in vacancy:
                        salary_from = vacancy["payment_from"]
                    if "payment_to" in vacancy:
                        salary_to = vacancy["payment_to"]
                    if "currency" in vacancy:
                        currency = vacancy["currency"]
                    if "vacancyRichText" in vacancy:
                        description = vacancy["vacancyRichText"]
                    if ("client" in vacancy) and ("url" in vacancy["client"]):
                        url = vacancy["client"]["url"]
                    if "firm_name" in vacancy:
                        firm_name = vacancy["firm_name"]

                if "name" in vacancy:
                    title = vacancy["name"]
                    service = "HH"
                    if vacancy["salary"] and ("salary" in vacancy) and ("from" in vacancy["salary"]):
                        salary_from = vacancy["salary"]["from"]
                    if vacancy["salary"] and ("salary" in vacancy) and ("to" in vacancy["salary"]):
                        salary_to = vacancy["salary"]["to"]
                    if vacancy["salary"] and ("salary" in vacancy) and ("currency" in vacancy["salary"]):
                        currency = vacancy["salary"]["currency"]
                    if "requirement" in vacancy:
                        description = vacancy["requirement"]
                    if "url" in vacancy:
                        url = vacancy["url"]
                    if ("employer" in vacancy) and ("name" in vacancy["employer"]):
                        firm_name = vacancy["employer"]["name"]
                new_vacancy = Vacancy(id, title, salary_from, salary_to, url, description, currency, firm_name, service)
                list_vacancies.append(new_vacancy)
    # else:

    print(len(vacancies))



def get_data_from_file(file_path: str):
    file_connector = Connector(file_path)
    try:
        file_connector.is_file_not_old(file_path)
    except:
        print("Файл устарел. Сделайте новый запрос.")
        input("Для продолжения нажмите любую клавишу.")

    get_vacations_from_file(file_path)
    input("Для продолжения нажмите любую клавишу.")
    return


def main():
    while True:
        clrscr()
        print("------Парсер вакансий------")
        print("Выберите нужное действие:")
        print("1 - Сделать запрос на сайт superjob.ru и сохранить данные в файл")
        print("2 - Сделать запрос на сайт hh.ru и сохранить данные в файл")
        print("3 - Получить данные из файла")
        print("4 - Выход.")
        # print("")
        # Для ввода параметров запроса нажмите 1. (Выход - ctrl + D)")
        try:
            result = input()
            match result:
                case ("1"):
                    get_from_sj(file_path)
                case ("2"):
                    get_from_hh(file_path)
                case ("3"):
                    get_data_from_file(file_path)
                case ("4"):
                    exit()

        except EOFError:
            exit()

    # get_from_hh(file_path)
    # get_from_hh(file_path)






if __name__ == "__main__":
    main()