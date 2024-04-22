# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Python Standard Libraries
import argparse
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
import context  # pylint: disable=unused-import
from spine.cli import args


class TestArgsToDict(unittest.TestCase):
    def setUp(self):
        self.argparser = argparse.ArgumentParser(description="Empty")

        self.args = []

    def process(self) -> object:
        return args.args_to_dict(self.argparser.parse_args(self.args))

    def test_valid_values(self):
        self.argparser.add_argument("--test", dest="test", default="hello")
        self.argparser.add_argument(
            "--testing", dest="testing", default="hello there"
        )

        self.assertDictEqual(
            self.process(), {"test": "hello", "testing": "hello there"}
        )

    def test_valid_value(self):
        self.args.extend(["--test", "testing"])

        self.argparser.add_argument("--test", dest="test", default="hello")

        self.assertDictEqual(self.process(), {"test": "testing"})

    def test_default(self):
        self.argparser.add_argument("--test", dest="test", default="hello")

        self.assertDictEqual(self.process(), {"test": "hello"})

    def test_empty(self):
        self.argparser.add_argument("--test", dest="test")

        self.assertDictEqual(self.process(), {"test": None})

    def test_none(self):
        self.assertDictEqual(self.process(), {})


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
