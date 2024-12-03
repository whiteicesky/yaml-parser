import unittest
from io import StringIO
import sys
from contextlib import redirect_stdout
from readFromFile import ConfigParser

class TestConfigParser(unittest.TestCase):

    def setUp(self):
        self.parser = ConfigParser()

    def test_single_constant(self):
        config_text = """def max_connections = 100;"""
        self.parser.parse(config_text)
        self.assertEqual(self.parser.constants, {"max_connections": 100})

    def test_simple_assignment(self):
        config_text = """max_connections = 100;"""
        result = self.parser.parse(config_text)
        self.assertEqual(result, {"max_connections": 100})

    def test_string_value(self):
        """Проверка строки как значения"""
        config_text = """server_name = "localhost";"""
        result = self.parser.parse(config_text)
        self.assertEqual(result, {"server_name": "localhost"})

    def test_array_value(self):
        config_text = """servers = ["localhost", "127.0.0.1", "192.168.1.1"];"""
        result = self.parser.parse(config_text)
        self.assertEqual(result, {"servers": ["localhost", "127.0.0.1", "192.168.1.1"]})

    def test_dict_value(self):
        config_text = """server = {
            host = "localhost",
            port = 8080
        };"""
        result = self.parser.parse(config_text)
        self.assertEqual(result, {"server": {"host": "localhost", "port": 8080}})

    def test_nested_structure(self):
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
        config_text = """server = {
            host = "localhost",
            port = 8080
        """
        with self.assertRaises(SyntaxError):
            self.parser.parse(config_text)

    def test_invalid_assignment(self):
        config_text = """max_connections 100;"""
        with self.assertRaises(SyntaxError):
            self.parser.parse(config_text)

    def test_invalid_constant_definition(self):
        config_text = """def max_connections 100;"""
        with self.assertRaises(SyntaxError):
            self.parser.parse(config_text)

if __name__ == "__main__":
    unittest.main()
