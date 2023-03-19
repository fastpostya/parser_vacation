import datetime
import os
import json
from json import JSONDecodeError
import pprint
# from vacancy import Vacancy


class Connector:
    """
    The Class Connector is  connector to the file.
    The file must be in json format.
    In method is_valid_json is cheking for:
     - file is in JSON-format
     -
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешней деградации
    :param data_file:str - the path to the json-file. It has getter and setter.
    :param text: str - the text from the file 
    """
    __data_file = None

    def __init__(self, path):
        self.data_file = path
        self.text = ""
        self.__connect()
        # self.elements = []

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
                # print("path=", path, " self.text=",self.text)
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
        creating more then <days> ago raises TimeoutError, in other case returns True"""
        file_time = os.path.getmtime(path)
        file_time = datetime.datetime.fromtimestamp(file_time)
        time_now = datetime.datetime.now()         
        time_delta = time_now - file_time
        if time_delta > datetime.timedelta(days=days):
            raise TimeoutError(f"Файл с данными устарел.\
 Пожалуйста, обновите его!")
            # return False
        return True

    @staticmethod
    def is_valid_json(text: str) -> bool | JSONDecodeError:
        """
        Raises JSONDecodeError if text is not JSON or 
        return True if json is correct.
        :param text: str - text for checking      
        """
        # try:
        text_json = json.loads(text)            
        # except JSONDecodeError:
            # Файл self.data_file содержит некорректные данные или пустой.
            # return False
        return True

    def save_date(self, text: str) -> None:
        """Saving data in file data_file"""
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(text, file)
            return text

    def __connect(self) -> str | Exception:
        """
        Cheking if file <path> exist, cheking file creating date and time.
        If file doesn't exist - it will be created.
        """
        if self.is_file_exist(self.data_file) and\
                self.is_file_not_old(self.data_file):
            self.text = self.read_file()
        return self.text

    def insert(self, data: str) -> str:
        """
        Insert date in file with saving it's structure
        """
        # open file and read date from file
        # file was checked while initialisation
        # self.read_file()
        # print(self.text)
        list_save = []
        if self.text == "":
            # empty file
            self.save_date(data)
            return data
        else:
            # not empty file
            date_from_file = json.loads(self.text)
            if isinstance(date_from_file, dict):
                # there is one element in file
                list_save.append(date_from_file)
            elif isinstance(date_from_file, list):
                # there are many elements in file
                for file_elements in date_from_file:
                    list_save.append(file_elements)
        if data != "" and self.is_valid_json(data):
            new_data = json.loads(data)
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

        self.save_date(list_save)
        return list_save

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ - это поле для
        фильтрации, а значение - это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        self.read_file()
        if self.text != "":
            date = json.loads(self.text)
            filtred_list = []
            for element in date:
                if isinstance(query, dict):
                    if dict.keys in element and dict.values == element[dict.keys]:
                        filtred_list.append(element)
            return filtred_list
        else:
            raise (KeyError("Неправильный формат JSON-файла"))

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запросу,
        как в методе select. Если в query передан пустой словарь, то
        
        функция удаления не сработает
        """
        pass

def del_file(path):
    file = open(path, "w", encoding="UTF-8")
    file.write('')
    file.close()

if __name__ == '__main__':

    # path_save = os.sep.join(["tests", "test_files", "new.json"])
    # text_json = json.loads(path_save) 
    # print(text_json)
    # print(type(text_json))

    path_insert = os.sep.join(["tests", "test_files", "test_insert.json"])
    # del_file(path_insert)

    # with open(path_insert, "r", encoding="utf-8") as file:
    #     text = file.read()
    # print(text)
    # with open(path_insert, "r", encoding="utf-8") as file:
    #     text = file.read()
    # print(text)
    # with open(path_insert, "r", encoding="utf-8") as file:
    #     text = file.read()
    # print(text)

    # ---SELECT---
    # path_select = os.sep.join(["tests", "test_files", "test_select.json"])
    # connector_select = Connector(path_select)
    # connector_select.select({"key6": "value6"})
    # print(connector_select.text)
# -------------------------
# ----INSERT----
    connector_insert = Connector(path_insert)
    connector_insert.insert('{"key4": "value4"}')
    print(connector_insert.text)
    # connector_insert.insert('{"key5": "value5"}')
    # print(connector_insert.text)
    # connector_insert.insert('{"key6": "value6"}')
    # print(connector_insert.text)
    # # # try:
    # connector_insert.insert('')
    # print(connector_insert.text)
    # except:
    #     pass
    # connector_insert.insert('{"key": "value2"}')
    # connector_insert.insert('[{"key": "value3"}, {"key": "value4"}]')
    # connector_insert.insert('{"key": "value5"}')
    # pprint.pprint(connector_insert.text)


    # path = os.sep.join(["tests", "test_files", "test_insert.json"])
    # connector = Connector(path)
    # print(connector.read_file())
    # connector.insert('[{"key": "value"}, {"key": "value1"}]')
    # path1 = connector.data_file
    # with open(path1, "r", encoding="utf-8") as file:
    #     text = file.read()
    # print("text=", text)

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

    # connector_save = Connector(os.sep.join(["tests", "test_files", "test_save.json"]))
    # connector_save.save_date('[{"key1": "value1"}, {"key2": "value2"}]')

        # path_old_file = os.sep.join(["tests", "test_files", 
        #     "result_hh.json"])
        # path_new = os.sep.join(["tests", "test_files", 
        #     "new.json"])

    #     print(df.is_file_not_old(path_old_file))
    #     print(df.is_file_not_old(path_new))
    # except TimeoutError as error:
    #     print(error)
    # except ValueError:
    #     print("Структура json-файла неверная. Невозможно прочитать данные.")
    # df.__connect()
    # df = Connector('df.json')

    # data_for_file = {'id': 1, 'title': 'tet'}

    # df.insert(data_for_file)
    # data_from_file = df.select(dict())
    # assert data_from_file == [data_for_file]

    # df.delete({'id':1})
    # data_from_file = df.select(dict())
    # assert data_from_file == []
