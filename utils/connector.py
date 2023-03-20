import datetime
import os
import json
from json import JSONDecodeError


class Connector:
    """
    The Class Connector is  connector to the file.
    The file must be in json format.

    Methods:
    - is_valid_json: bool - cheking if file is in JSON-format.
    - is_file_exist: bool -cheking if file exists
    - read_file: str - getting text from file data_file
    - is_file_not_old: bool - checking if file not older than number days
    - save_date: str - saving data in file data_file
    - insert: str - insert date in file with saving it's structure.
    - select: list | KeyError - selecting dates from file.
        The key is the field for filtering. The value is the desired value.
    - delete: list | KeyError - deleting date, using query.

    Atributes:
    :param data_file:str - the path to the json-file. It has getter and setter.
    :param text: str - the text from the file
    :param save_date: list - list for saving in file
    :param delete_query: dict - dict for deleting data
    :param select_query: dict - dict for selection data
    :param
    """
    __data_file = None

    def __init__(self, path):
        self.data_file = path
        self.text = ""
        self.list_select = ""
        self.select_query = {}
        self.delete_query = {}
        self.__connect()

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, path: str) -> bool:
        # код для установки файла
        self.__data_file = path
        return self.__data_file

    @staticmethod
    def is_file_exist(path: str) -> bool:
        """Cheking if file <path> exist and return True or False"""
        return os.path.exists(path)

    def read_file(self) -> str:
        """ Open the file data_file and returns it's text"""
        path = self.data_file
        if self.is_file_exist(path):
            with open(path, "r", encoding="utf-8") as file:
                text = file.read()
                self.text = text
            return self.text
        else:
            # file does not exist, let's create it
            file = open(path, "w", encoding="utf-8")
            file.write("")
            file.close()
            return ""

    @staticmethod
    def is_file_not_old(path: str, days: int = 1) -> bool | TimeoutError:
        """ Cheking file creating date and time. If the file was
        creating more then <days> ago raises TimeoutError,
        in other case returns True
        """
        file_time = os.path.getmtime(path)
        file_time = datetime.datetime.fromtimestamp(file_time)
        time_now = datetime.datetime.now()
        time_delta = time_now - file_time
        if time_delta > datetime.timedelta(days=days):
            raise TimeoutError("Файл с данными устарел.\
 Пожалуйста, обновите его!")
        return True

    @staticmethod
    def is_valid_json(text: str) -> bool | JSONDecodeError:
        """
        Raises JSONDecodeError if text is not JSON or
        return True if json is correct.
        :param text: str - text for checking
        """
        text_json = json.loads(text)
        return True

    def save_date(self, data: dict | list) -> None:
        """Saving data in file data_file"""
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
            return data

    def __connect(self) -> str | Exception:
        """
        Cheking if file <path> exist, cheking file creating date and time.
        If file doesn't exist - it will be created.
        """
        # if self.is_file_exist(self.data_file):
        #  and self.is_file_not_old(self.data_file):
        self.text = self.read_file()
        return self.text

    def insert(self, data: str) -> str:
        """
        Insert date in file with saving it's structure.
        :param data: str - date in JSON format.
        In case empty or wrong date raises KeyError.
        Returns text - date with insertion.
        """
        # open file and read date from file
        # file was checked while initialisation
        list_save = []
        if self.text != "":
            # not empty file
            date_from_file = json.loads(self.text)
            if isinstance(date_from_file, dict):
                # there is one element in file
                list_save.append(date_from_file)
            elif isinstance(date_from_file, list):
                # there are many elements in file
                for file_elements in date_from_file:
                    list_save.append(file_elements)
        if data: # != "" and self.is_valid_json(data):
            # new_data = json.loads(data)
            new_data = data
            if isinstance(new_data, dict):
                # new_date is one element
                list_save.append(new_data)
            elif isinstance(new_data, list):
                # there are many elements in new_data
                for element in new_data:
                    list_save.append(element)
            else:
                raise KeyError("Некорректные данные")
        else:
            raise KeyError("Некорректные данные")
        if len(list_save) == 1:
            self.save_date(list_save[0])
            self.text = json.dumps(list_save[0], ensure_ascii=False)
        else:
            self.save_date(list_save)
            self.text = json.dumps(list_save, ensure_ascii=False)
        return self.text

    def select(self, query: dict) -> list | KeyError:
        """
        Selecting dates from file.
        :param query:dict - the dictinary for selection date.
        Selected dates are saving in list_select
        The key is the field for filtering. The value is the desired value.
        Example:
        {'price': 1000} return only dictionary that contain the field 'price'
        and price is equal 1000.
        In case query contain more or less than 1 pair key/value
        or file is empty raises KeyError.
        """
        self.select_query = query
        self.read_file()
        self.list_select = []
        if self.text != "":
            date = json.loads(self.text)
            self.list_select = []
            if isinstance(query, dict) and len(query) == 1:
                first_key = list(query.keys())[0]
                first_value = query[first_key]
                for element in date:
                    if first_key in element and first_value ==\
                            element[first_key]:
                        self.list_select.append(element)

                return self.list_select
            else:
                raise (KeyError("Неправильный формат \
словаря для отбора данных"))
        else:
            raise (KeyError("Неправильный формат JSON-файла"))

    def delete(self, query: dict) -> list | KeyError:
        """
        Deleting date, using query.
        :param query:dict - the dictinary for deleting date.
        The key is the field for filtering. The value is the desired value.
        In case query contain more or less than 1 pair key/value
        or file is empty raises KeyError.
        """
        self.delete_query = query
        self.read_file()
        if self.text != "":
            date = json.loads(self.text)
            new_list = []
            if isinstance(query, dict) and len(query) == 1:
                first_key = list(query.keys())[0]
                first_value = query[first_key]
                for element in date:
                    if not (first_key in element and first_value ==\
                            element[first_key]):
                        new_list.append(element)
                self.save_date(new_list)
                self.text = json.dumps(new_list, ensure_ascii=False)
                return new_list
            else:
                raise (KeyError("Неправильный формат словаря для отбора данных"))
        else:
            raise (KeyError("Неправильный формат JSON-файла"))


def del_file(path):
    file = open(path, "w", encoding="UTF-8")
    file.write('')
    file.close()


def try_insert():
    path_insert = os.sep.join(["tests", "test_files", "test_insert.json"])
    # clear file
    del_file(path_insert)
    # ----INSERT----
    connector_insert = Connector(path_insert)
    connector_insert.insert({"key4": "value4"})
    print(connector_insert.text)
    connector_insert.insert({"key5": "value5"})
    print(connector_insert.text)
    try:
        connector_insert.insert([{"key6": "value6"}, {"text1": "1235"}])
        print(connector_insert.text)
    except:
        print('ERROR: [{"key6": "value6"}, {"text1": "1235"}]')
    try:
        connector_insert.insert([{"key6": "value6", "text2": "4587"}])
        print(connector_insert.text)
    except:
        print('ERROR: [{"key6": "value6", "text2": "4587"}]')
    try:
        connector_insert.insert([{"key6": "value6", "tex32": "2587"}])
        print(connector_insert.text)
    except:
        print('ERROR: [{"key6": "value6", "tex32": "2587"}]')
    # # # try:
    # connector_insert.insert('')
    # print(connector_insert.text)
    # except:
    #     pass
    # connector_insert.insert('{"key": "value2"}')
    # connector_insert.insert('[{"key": "value3"}, {"key": "value4"}]')
    # connector_insert.insert('{"key": "value5"}')
    # pprint.pprint(connector_insert.text)


def try_select():
    # ---SELECT---
    path_select = os.sep.join(["tests", "test_files", "test_select.json"])
    connector_select = Connector(path_select)
    connector_select.select({"key6": "value6"})
    print(connector_select.list_select)


def try_delete():
    path_delete = os.sep.join(["tests", "test_files", "test_delete.json"])
    del_file(path_delete)
    connector_del = Connector(path_delete)
    connector_del.insert([{"key4": "value4"}, {"key5": "value5"}, {"key6": "value6"}, {"text1": "1235"}, {"key6": "value6", "text2": "4587"}])
    connector_del.delete({"text1": "1235"})
    connector_del.delete({"key5": "value5"})
    connector_del.delete({"key4": "value4"})
    connector_del.delete({"key6": "value6"})
    connector_del.insert([{"key4": "value4"}, {"key5": "value5"}, {"key6": "value6"}, {"text1": "1235"}, {"key6": "value6", "text2": "4587"}])

    print(connector_del.text)

if __name__ == '__main__':
    # try_insert()
    try_select()
    # try_delete()


    # try:
        # df = Connector(os.sep.join(["vacations.json"]))
    #     path = os.sep.join(["tests", "test_files", "new.json"])
    #     file = open(path, "w", encoding="UTF-8")
    #     file.write('[{"key1": "value1"}, {"key2": "value2"}]')
    #     file.close()
    #     df = Connector(path)
    #     print(df.text)
    # except JSONDecodeError:
    #     print("Неверный формат JSON")
    # except TimeoutError:
    #     print("Файл устарел")