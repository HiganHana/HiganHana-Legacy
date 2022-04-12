from pprint import pprint
import unittest
from lib.config import Config

class t_config(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config()

    def test_storage_rule(self):
        self.config.test1 = "test1"
        self.config._test0 = "test0"

        pprint(self.config.__dict__)

        self.assertEqual(self.config.test1, "test1")
        self.assertEqual(self.config._test0, "test0")
        self.assertEqual(self.config._config["test1"], "test1")