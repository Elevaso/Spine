# pyright: reportMissingImports=false

# Python Standard Libraries
import context
import inspect
from inspect import FrameInfo
import os
import unittest
from unittest import mock

# 3rd Party Libraries


# Code Repository Sub-Packages
from spine.app import caller


def mock_inspect():
    return [
        FrameInfo(
            inspect.currentframe(),
            os.path.split(__file__)[0],
            25,
            TestGetCaller.test_caller,
            ["unittest.main() # pragma: no cover\n"],
            0,
        )
    ]


class TestGetCaller(unittest.TestCase):
    def test_caller(self):
        with mock.patch("inspect.stack", new=mock_inspect):
            val = caller.get_caller()

        self.assertIsInstance(val, tuple)
        self.assertIn("test_app_caller.py", val[0])
        self.assertIn("unit", val[1])
        self.assertTrue(os.path.exists(val[0]))
        self.assertTrue(os.path.exists(val[1]))


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
