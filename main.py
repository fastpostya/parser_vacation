from config import super_job_key, keyword
from utils.superjob import Superjob
from utils.no_vac_error import NoVacationError
import pprint


def main():
    # Создаем экземпляр класса Superjob для поиска вакансий на сайте superjob
    superjob = Superjob()
    try:
        superjob.get_request("Pyton", "Краснодар")
        superjob.print_info()
    except ConnectionError as error:
        print(error)
    except NoVacationError as error:
        print(error)


if __name__ == "__main__":
    main()