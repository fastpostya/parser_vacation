import json
from utils.connector import Connector
from utils.vacancy import Vacancy


def get_vacations_from_file(file_path: str):
    list_vacancies = []
    connector = Connector(file_path)
    connector.read_file()
    response = json.loads(connector.text)
    if isinstance(response, dict):
        # only one vacancy
        vacancies = []
        vacancies.append(response)
    else:
        vacancies = response
    if vacancies:
        for vacancy in vacancies:
            if "id" in vacancy:
                # no new instance Vacancy without id
                id = vacancy["id"]
                title = ""
                salary_from = 0.0
                salary_to = 0.0
                url = ""
                description = ""
                currency = ""
                firm_name = ""
                service = ""
                if "profession" in vacancy:
                    title = vacancy["profession"]
                    service = "SJ"
                    if ("payment_from" in vacancy) and vacancy["payment_from"]:
                        salary_from = float(vacancy["payment_from"])
                    if ("payment_to" in vacancy) and vacancy["payment_to"]:
                        salary_to = float(vacancy["payment_to"])
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
                    if vacancy["salary"] and ("salary" in vacancy) and\
                        ("from" in vacancy["salary"])\
                        and vacancy["salary"]["from"]:
                        salary_from = float(vacancy["salary"]["from"])
                    if vacancy["salary"] and ("salary" in vacancy) and\
                        ("to" in vacancy["salary"])\
                        and vacancy["salary"]["to"]:
                        salary_to = float(vacancy["salary"]["to"])
                    if vacancy["salary"] and ("salary" in vacancy) and\
                        ("currency" in vacancy["salary"]):
                        currency = vacancy["salary"]["currency"]
                    if "requirement" in vacancy:
                        description = vacancy["requirement"]
                    if "url" in vacancy:
                        url = vacancy["url"]
                    if ("employer" in vacancy) and\
                        ("name" in vacancy["employer"])\
                        and vacancy["employer"]["name"]:
                        firm_name = vacancy["employer"]["name"]
                if salary_to != 0.0:
                    salary = salary_to
                else:
                    salary = salary_from
                new_vacancy = Vacancy(
                    id, title, salary_from, salary_to,
                    salary, url, description, currency,
                    firm_name, service)
                list_vacancies.append(new_vacancy)
    return list_vacancies
