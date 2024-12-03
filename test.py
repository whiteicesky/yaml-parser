import unittest
from io import StringIO
import sys
from contextlib import redirect_stdout
from main import ConfigParser  # Импортируем парсер из основного файла

class TestConfigParser(unittest.TestCase):

    def setUp(self):
        """Этот метод вызывается перед каждым тестом"""
        self.parser = ConfigParser()

    def test_single_constant(self):
        """Проверка обработки одной константы"""
        config_text = """def max_connections = 100;"""
        self.parser.parse(config_text)
        self.assertEqual(self.parser.constants, {"max_connections": 100})

    def test_simple_assignment(self):
        """Проверка простого присваивания"""
        config_text = """max_connections = 100;"""
        result = self.parser.parse(config_text)
        self.assertEqual(result, {"max_connections": 100})

    def test_string_value(self):
        """Проверка строки как значения"""
        config_text = """server_name = "localhost";"""
        result = self.parser.parse(config_text)
        self.assertEqual(result, {"server_name": "localhost"})

    def test_array_value(self):
        """Проверка массива значений"""
        config_text = """servers = ["localhost", "127.0.0.1", "192.168.1.1"];"""
        result = self.parser.parse(config_text)
        self.assertEqual(result, {"servers": ["localhost", "127.0.0.1", "192.168.1.1"]})

    def test_dict_value(self):
        """Проверка словаря как значения"""
        config_text = """server = {
            host = "localhost",
            port = 8080
        };"""
        result = self.parser.parse(config_text)
        self.assertEqual(result, {"server": {"host": "localhost", "port": 8080}})

    def test_nested_structure(self):
        """Проверка вложенных структур (массивы и словари)"""
        config_text = """server = {
            host = "localhost",
            routes = [
                {path = "/", handler = "index"},
                {path = "/about", handler = "about"}
            ]
        };"""
        result = self.parser.parse(config_text)
        self.assertEqual(result, {
            "server": {
                "host": "localhost",
                "routes": [
                    {"path": "/", "handler": "index"},
                    {"path": "/about", "handler": "about"}
                ]
            }
        })

    def test_constant_inclusion(self):
        """Проверка, что константы появляются в начале"""
        config_text = """def max_connections = 100;
        server = {
            host = "localhost",
            port = 8080
        };"""
        result = self.parser.parse(config_text)
        self.assertEqual(result, {
            "max_connections": 100,
            "server": {
                "host": "localhost",
                "port": 8080
            }
        })

    def test_syntax_error_missing_bracket(self):
        """Проверка на ошибку при пропущенной закрывающей скобке"""
        config_text = """server = {
            host = "localhost",
            port = 8080
        """
        with self.assertRaises(SyntaxError):
            self.parser.parse(config_text)

    def test_invalid_assignment(self):
        """Проверка на ошибку в случае неверного синтаксиса присваивания"""
        config_text = """max_connections 100;"""
        with self.assertRaises(SyntaxError):
            self.parser.parse(config_text)

    def test_invalid_constant_definition(self):
        """Проверка на ошибку в случае неверного синтаксиса определения константы"""
        config_text = """def max_connections 100;"""
        with self.assertRaises(SyntaxError):
            self.parser.parse(config_text)

if __name__ == "__main__":
    unittest.main()
