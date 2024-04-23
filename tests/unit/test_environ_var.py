# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Python Standard Libraries
import os
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
import context  # pylint: disable=unused-import
from spine.environ import var


class TestGetVar(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["hello"] = "world"

    def test_exists(self):
        val = var.get_var("hello")

        self.assertIsInstance(val, str)
        self.assertEqual(val, "world")

    def test_not_exists(self):
        val = var.get_var("hello1")

        self.assertIsNone(val)


class TestSetVar(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["hello"] = "world"

    def call_func(self, name, val, **kwargs) -> context.Tuple[str, str]:
        overwrite = kwargs.get("overwrite", False)
        set_val = kwargs.get("set_val", True)
        level = kwargs.get("level", "DEBUG")

        with self.assertLogs(level=level) as log:
            val = var.set_var(name, val, overwrite, set_val)

        return log, val

    def test_not_exists(self):
        _, val = self.call_func("hello1", "world")

        self.assertIsInstance(val, bool)
        self.assertTrue(val)
        self.assertEqual(os.environ["hello1"], "world")

    def test_overwrite(self):
        self.assertEqual(os.environ["hello"], "world")

        _, val = self.call_func("hello", "there", overwrite=True)

        self.assertIsInstance(val, bool)
        self.assertTrue(val)
        self.assertEqual(os.environ["hello"], "there")

    def test_no_overwrite(self):
        self.assertEqual(os.environ["hello"], "world")

        log, val = self.call_func("hello", "there", level="DEBUG")

        self.assertIsInstance(val, bool)
        self.assertFalse(val)
        self.assertEqual(os.environ["hello"], "world")
        self.assertIn(
            "Overwrite is False, skipping environment variable hello",
            log.output[0],
        )

    def test_mock(self):
        self.assertEqual(os.environ["hello"], "world")

        val = var.set_var("hello", "there", set_val=False)

        self.assertIsInstance(val, bool)
        self.assertTrue(val)
        self.assertEqual(os.environ["hello"], "world")


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
