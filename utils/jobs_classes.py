from utils.vacancy import Vacancy
from utils.no_vac_error import NoVacationError


def sorting(vacancies: list) -> list:
    """
    Sorting the list of vacancies by salary.
    param: vacancies: list
    Returns sorted list of vacancies
    """
    if len(vacancies) == 0:
        raise NoVacationError("Нет вакансий для сортировки")
    sorted_list = sorted(vacancies, key=lambda x: x.salary, reverse=True)
    return sorted_list


def get_top(vacancies: list, top_count: int) -> list:
    """ Returns {top_count} vacancies, sorted by salary
    param: vacancies: list
    param: top_count: int
    """
    if len(vacancies) == 0:
        raise NoVacationError("Нет вакансий для вывода")
    sorted_list = sorted(vacancies, key=lambda x: x.salary, reverse=True)
    top_count = min(top_count, len(sorted_list))
    new_list = []
    for i in range(top_count):
        new_list.append(sorted_list[i])
    return new_list