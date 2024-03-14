# pyright: reportMissingImports=false

# Python Standard Libraries
import context
import os
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
from spine.environ import var


class TestGet(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["hello"] = "world"

    def test_exists(self):
        val = var.get("hello")

        self.assertIsInstance(val, str)
        self.assertEqual(val, "world")

    def test_not_exists(self):
        val = var.get("hello1")

        self.assertIsNone(val)


class TestSet(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["hello"] = "world"

    def call_func(
        self, name, val, overwrite=False, set_val=True, level="DEBUG"
    ) -> context.Tuple[str, str]:
        with self.assertLogs(level=level) as log:
            val = var.set(name, val, overwrite, set_val)

        return log, val

    def test_not_exists(self):
        _, val = self.call_func("hello1", "world")

        self.assertIsInstance(val, bool)
        self.assertTrue(val)
        self.assertEqual(os.environ["hello1"], "world")

    def test_overwrite(self):
        self.assertEqual(os.environ["hello"], "world")

        _, val = self.call_func("hello", "there", True)

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

        val = var.set("hello", "there", set_val=False)

        self.assertIsInstance(val, bool)
        self.assertTrue(val)
        self.assertEqual(os.environ["hello"], "world")


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
