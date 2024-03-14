# pyright: reportMissingImports=false

# Python Standard Libraries
import context
import os
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
from spine.app import caller


class TestGetCaller(unittest.TestCase):
    def test_caller(self):
        val = caller.get_caller()

        self.assertIsInstance(val, tuple)
        self.assertIn("test_app_caller.py", val[0])
        self.assertIn("unit", val[1])
        self.assertTrue(os.path.exists(val[0]))
        self.assertTrue(os.path.exists(val[1]))


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
