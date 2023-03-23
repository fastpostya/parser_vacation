from json import JSONDecodeError
import click
from config import keyword, file_path
from utils.superjob import Superjob
from utils.hh import HH
from utils.no_vac_error import NoVacationError
from utils.connector import Connector
from utils.func import get_vacations_from_file
from utils.jobs_classes import sorting, get_top


def clrscr():
    # Clear screen using click.clear() function
    click.clear()


def get_from_sj(file_path: str):
    """Get request from superjob.ru and insert date in file 'file_path'"""
    print("Делаем запрос на сайт Superjob")
    clear = input("Очистить файл?\nПодтвердите очистку - y")

    # Создаем экземпляр класса Superjob для поиска вакансий на сайте superjob
    superjob = Superjob()
    try:
        answer = superjob.get_request(keyword)  # , "Магадан")
    except ConnectionError as error:
        print(error)
        input("Для продолжения нажмите любую клавишу.")
        return
    except NoVacationError as error:
        print(error)
        input("Для продолжения нажмите любую клавишу.")
        return

    connector = superjob.get_connector(file_path)
    if clear == "y":
        connector.save_date(None)

    try:
        connector.insert(answer)
    except KeyError as error:
        print(error)
        input("Для продолжения нажмите любую клавишу.")
        return
    except JSONDecodeError as error:
        print(error)
        input("Для продолжения нажмите любую клавишу.")
        return


def get_from_hh(file_path: str):
    """Get request from hh.ru and insert date in file 'file_path'"""
    print("Делаем запрос на сайт hh.ru")
    clear = input("Очистить файл?\nПодтвердите очистку - y")
    # Создаем экземпляр класса HHVacancy
    hh = HH()
    try:
        answer = hh.get_request(keyword)
    except ConnectionError as error:
        print(error)
        input("Для продолжения нажмите любую клавишу.")
        return
    except NoVacationError as error:
        print(error)
        input("Для продолжения нажмите любую клавишу.")
        return
    connector_hh = hh.get_connector(file_path)
    if clear == "y":
        connector_hh.save_date(None)
    try:
        connector_hh.insert(answer)
    except KeyError as error:
        print(error)
        input("Для продолжения нажмите любую клавишу.")
        return
    except JSONDecodeError as error:
        print(error)
        input("Для продолжения нажмите любую клавишу.")
        return


def delete_data_firm_name(file_path: str):
    param = input("Введите название организации для удаления из файла\n")
    connector = Connector(file_path)
    try:
        connector.delete({"firm_name": param})
    except KeyError as error:
        print(error)
    print(f"Вакансии от {param} удалены")
    input("Для продолжения нажмите любую клавишу.")


def get_data_from_file(file_path: str):
    list_vacancies = []
    file_connector = Connector(file_path)
    try:
        file_connector.is_file_not_old(file_path)
    except TimeoutError:
        clrscr()
        print("Файл устарел. Сделайте новый запрос.")
        input("Для продолжения нажмите любую клавишу.")

    try:
        list_vacancies = get_vacations_from_file(file_path)
    except JSONDecodeError:
        print("Неправильный формат данных в файле. Пожалуйста, сделайте новый запрос.")
        input("Для продолжения нажмите любую клавишу.")
        return
    clrscr()
    print("Выберите нужное действие:")
    print("1 - Напечатать вакансии")
    print("2 - Отсортировать вакансии по зарплате.")
    print("3 - Вывести 10 вакансий с наивысшей оплатой.")
    result = input()

    match result:
        case ("1"):
            if len(list_vacancies):
                print("Вакансий в файле:", len(list_vacancies))
                for i in list_vacancies:
                    print(i)
            else:
                print("Вакансий в файле не найдено. Создайте новый запрос.")
            input("Для продолжения нажмите любую клавишу.")
        case ("2"):
            try:
                sorted_list = sorting(list_vacancies)
                for i in sorted_list:
                    print(i)
            except NoVacationError as error:
                print(error)
            input("Для продолжения нажмите любую клавишу.")
        case ("3"):
            try:
                top_vacancies = get_top(list_vacancies, 10)
                for i in top_vacancies:
                    print(i)
            except NoVacationError as error:
                print(error)
            input("Для продолжения нажмите любую клавишу.")


def main():
    while True:
        clrscr()
        print("------Парсер вакансий------")
        print("Выберите нужное действие:")
        print("1 - Сделать запрос на сайт superjob.ru и сохранить данные в файл")
        print("2 - Сделать запрос на сайт hh.ru и сохранить данные в файл")
        print("3 - Получить данные из файла")
        print("4 - Удалить вакансии от заданной организации")
        print("5 - Выход.")
        # (Выход - ctrl + D)
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
                    delete_data_firm_name(file_path)
                case ("5"):
                    exit()

        except EOFError:
            exit()


if __name__ == "__main__":
    main()
