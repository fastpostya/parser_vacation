from utils.vacancy import Vacancy


def sorting(vacancies: list) -> list:
    """
    Sorting the list of vacancies by salary.
    param: vacancies: list
    Returns sorted list of vacancies
    ?????(gt, lt magic methods)
    """
    sorted_list = sorted(vacancies, key=lambda x: x.salary, reverse=True)
    return sorted_list


def get_top(vacancies: list, top_count: int) -> list:
    """ Returns {top_count} vacancies, sorted by salary
    param: vacancies: list
    param: top_count: int
    (iter, next magic methods) """
    sorted_list = sorted(vacancies, key=lambda x: x.salary, reverse=True)
    new_list = []
    for i in range(top_count):
        new_list.append(sorted_list[i])
    return new_list