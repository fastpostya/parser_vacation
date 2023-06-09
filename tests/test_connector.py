from json import JSONDecodeError
import os
import unittest
from utils.connector import Connector


class Test_Connector(unittest.TestCase):
    """Class for testing class Connector."""

    def setUp(self):
        """setting initial values"""
        self.path_open = os.sep.join(["tests", "test_files", "test_open.json"])
        self.path_no_exist = os.sep.join(
            ["tests", "test_files", "nofile.json"])
        self.path_no_exist_and_del = os.sep.join(
            ["tests", "test_files", "nofile1.json"])
        self.path_old_file = os.sep.join(
            ["tests", "test_files", "result_hh.json"])
        self.path_new = os.sep.join(
            ["tests", "test_files", "new.json"])
        # create new file for testing
        file = open(self.path_new, "w", encoding="UTF-8")
        file.write('[{"key1": "value1"}, {"key2": "value2"}]')
        file.close()

        self.path_empty_insert = os.sep.join(
            ["tests", "test_files", "test__empty_insert.json"])
        file = open(self.path_empty_insert, "w", encoding="UTF-8")
        file.write('')
        file.close()

        self.path_save = os.sep.join(["tests", "test_files", "test_save.json"])
        self.valid_json = [{"key1": "value1"}, {"key2": "value2"}]
        self.connector = Connector(self.path_new)

        self.path_select = os.sep.join(
            ["tests", "test_files", "test_select.json"])
        # create new file for testing
        file = open(self.path_select, "w", encoding="UTF-8")
        file.write('')
        file.close()

        self.path_del = os.sep.join(
            ["tests", "test_files", "test_delete.json"])

        # create new file for testing
        file = open(self.path_del, "w", encoding="UTF-8")
        file.write('')
        file.close()

        self.path_ins_unic = os.sep.join(
            ["tests", "test_files", "test_ins_unic.json"])

        # create new file for testing
        file = open(self.path_ins_unic, "w", encoding="UTF-8")
        file.write('')
        file.close()

    def test__init__(self) -> None:
        """Testing initialising instanse of class Connector.
        testing if path exist and is actual. Else raises
        JSONDecodeError or TimeoutError.
        """
        self.assertEqual(
            self.connector.data_file,
            os.sep.join(["tests", "test_files", "new.json"])
            )

    def test_read_file(self) -> None:
        """Test if file exist - read and return text,
        if not - create it and return '' """
        self.assertEqual(
            self.connector.read_file(),
            '[{"key1": "value1"}, {"key2": "value2"}]')
        self.assertEqual(
            self.connector.text,
            '[{"key1": "value1"}, {"key2": "value2"}]')
        connector_del = Connector(self.path_no_exist_and_del)
        self.assertEqual(connector_del.read_file(), '')

        # del file self.path_no_exist_and_del after testing
        if os.path.isfile(self.path_no_exist_and_del):
            os.remove(self.path_no_exist_and_del)

    def test_is_file_not_old(self) -> None:
        """test if file was create more than 24-h til now"""
        self.assertTrue(self.connector.is_file_not_old(self.path_new))
        with self.assertRaises(TimeoutError):
            self.connector.is_file_not_old(self.path_old_file)

    def test_is_valid_json(self) -> None:
        """testing is json correct"""
        self.assertTrue(self.connector.is_valid_json('[{"key1": "value1"},\
 {"key2": "value2"}]'))
        self.assertTrue(self.connector.is_valid_json('{"key1": "value1"}'))
        self.assertTrue(self.connector.is_valid_json('{}'))
        with self.assertRaises(JSONDecodeError):
            self.connector.is_valid_json('')
        with self.assertRaises(JSONDecodeError):
            self.connector.is_valid_json('[{value1}, {"key2": "value2"}]')
        with self.assertRaises(JSONDecodeError):
            self.connector.is_valid_json('[{"key1": "value1"}, {"value2"}]')

    def test_save_date(self) -> None:
        """testing saving file"""
        connector_save = Connector(self.path_save)
        connector_save.save_date(self.valid_json)
        self.assertTrue(os.path.exists(self.path_save))

    def test_insert(self) -> None:
        """testing inserting in empty file and not empty"""
        self.connector_insert = Connector(self.path_empty_insert)

        # wrong data not list, not dict
        with self.assertRaises(KeyError):
            self.connector_insert.insert("key")

        # first insert
        self.connector_insert.insert({"key": "value"})
        with open(self.path_empty_insert, "r", encoding="utf-8") as file:
            text_from_file = file.read()
        self.assertEqual('{"key": "value"}', text_from_file)

        # second insert
        self.connector_insert.insert({"key1": "value1"})
        with open(self.path_empty_insert, "r", encoding="utf-8") as file:
            text_from_file = file.read()
        self.assertEqual(
            '[{"key": "value"}, {"key1": "value1"}]',
            text_from_file)

        # third insert
        self.connector_insert.insert({"key2": "value2"})
        with open(self.path_empty_insert, "r", encoding="utf-8") as file:
            text_from_file = file.read()
        self.assertEqual(
            '[{"key": "value"}, {"key1": "value1"}, {"key2": "value2"}]',
            text_from_file)
        with self.assertRaises(KeyError):
            self.connector_insert.insert("")
        with self.assertRaises(KeyError):
            self.connector_insert.insert([])
        with self.assertRaises(KeyError):
            self.connector_insert.insert({})

        # create empty file
        file = open(self.path_empty_insert, "w", encoding="UTF-8")
        file.write('')
        file.close()
        self.connector_insert = Connector(self.path_empty_insert)
        self.connector_insert.insert([
            {"key": "value"},
            {"key1": "value1"}
            ])
        with open(self.path_empty_insert, "r", encoding="utf-8") as file:
            text_from_file = file.read()
        self.assertEqual(
                        '[{"key": "value"}, {"key1": "value1"}]',
                        text_from_file)

    def test_select(self) -> None:
        """testing selection from file"""
        self.connector_select = Connector(self.path_select)

        # trying selectin in empty file
        with self.assertRaises(KeyError):
            self.connector_select.select({"key": "value"})
        self.connector_select.insert([
                                    {"key4": "value4", "key6": "value6"},
                                    {"key5": "value5"},
                                    {"key5": "value6", "text1": "1235"},
                                    {"key6": "value6", "text2": "4587"},
                                    {"key6": "value6", "tex32": "2587"}
        ])

        # wrong data not list, not dict
        with self.assertRaises(KeyError):
            self.connector_select.select("key")

        text_select = self.connector_select.select({"key6": "value6"})
        self.assertEqual(text_select, [
                {"key4": "value4", "key6": "value6"},
                {"key6": "value6", "text2": "4587"},
                {"key6": "value6", "tex32": "2587"}
                ])

    def test_delete(self) -> None:
        """testin deleting file by query"""
        self.connector_del = Connector(self.path_del)

        # deleting from empty file
        with self.assertRaises(KeyError):
            self.connector_del.delete({"key5": "value5"})

        self.connector_del.insert(
            [
                {"key4": "value4", "key6": "value6"},
                {"key5": "value5"},
                {"key5": "value6", "text1": "1235"},
                {"key6": "value6", "text2": "4587"},
                {"key6": "value6", "tex32": "2587"}
                ]
            )
        self.connector_del.delete({"key5": "value5"})
        with open(self.path_del, "r", encoding="utf-8") as file:
            text_from_file = file.read()
        self.assertEqual(
            text_from_file,
            '[{"key4": "value4", "key6": "value6"}, {"key5": "value6",\
 "text1": "1235"}, {"key6": "value6", "text2": "4587"}, {"key6":\
 "value6", "tex32": "2587"}]')
        self.connector_del.delete({"key4": "value4"})
        with open(self.path_del, "r", encoding="utf-8") as file:
            text_from_file = file.read()
        self.assertEqual(text_from_file, '[{"key5": "value6",\
 "text1": "1235"}, {"key6": "value6", "text2": "4587"}, {"key6":\
 "value6", "tex32": "2587"}]')
        with self.assertRaises(KeyError):
            self.connector_del.delete({})
        with self.assertRaises(KeyError):
            self.connector_del.delete("")

    def test_id_is_not_in_data(self) -> None:
        """Check if id in data"""
        connector = Connector(self.path_open)
        test_dict1 = {"id": "123"}
        test_dict2 = {"key": "123"}
        self.assertTrue(connector.id_is_in_data(test_dict1, "123"))
        self.assertFalse(connector.id_is_in_data(test_dict1, "125"))
        self.assertFalse(connector.id_is_in_data(test_dict2, "123"))

        test_list1 = [{"id": "123"}, {"key": "123"}, {"id": "124"}]
        test_list2 = [{"key": "123"}, {"key": "125"}, {"key": "124"}]
        self.assertTrue(connector.id_is_in_data(test_list1, "123"))
        self.assertTrue(connector.id_is_in_data(test_list1, "124"))
        self.assertFalse(connector.id_is_in_data(test_list1, "125"))
        self.assertFalse(connector.id_is_in_data(test_list2, "123"))

    def test_insert_unic(self) -> None:
        """Insert only dict with inic id"""
        connector = Connector(self.path_ins_unic)
        connector.insert_only_unic({"id": "123"})
        with open(self.path_ins_unic, "r", encoding="utf-8") as file:
            text_from_file = file.read()
        self.assertEqual(
                        '{"id": "123"}',
                        text_from_file)

        # try to add the same data
        connector.insert_only_unic({"id": "123"})
        with open(self.path_ins_unic, "r", encoding="utf-8") as file:
            text_from_file = file.read()
        self.assertEqual(
                        '{"id": "123"}',
                        text_from_file)
        connector.insert_only_unic({"id": "124"})
        connector.insert_only_unic({"id": "125"})
        connector.insert_only_unic({"id": "125"})
        with open(self.path_ins_unic, "r", encoding="utf-8") as file:
            text_from_file = file.read()
        self.assertEqual(
                        '[{"id": "123"}, {"id": "124"}, {"id": "125"}]',
                        text_from_file)

        connector.insert_only_unic({"key": "125"})
        with open(self.path_ins_unic, "r", encoding="utf-8") as file:
            text_from_file = file.read()
        self.assertEqual(
            '[{"id": "123"}, {"id": "124"}, {"id": "125"}, {"key": "125"}]',
            text_from_file)

        # inserting the same data
        connector.insert_only_unic([{"id": "125"}, {"id": "123"}])
        with open(self.path_ins_unic, "r", encoding="utf-8") as file:
            text_from_file = file.read()
        self.assertEqual(
            '[{"id": "123"}, {"id": "124"}, {"id": "125"}, {"key": "125"}]',
            text_from_file)

        with self.assertRaises(KeyError):
            connector.insert_only_unic("key")
