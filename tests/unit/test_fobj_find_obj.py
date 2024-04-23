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
from spine.fobj import find_obj


class TestCheck(unittest.TestCase):
    def test_found(self):
        val = find_obj.check(os.path.dirname(__file__), "context.py")

        self.assertTrue(val)

    def test_not_found(self):
        with self.assertLogs(level="WARN") as log:
            val = find_obj.check(
                os.path.dirname(__file__), "hello.world"
            )

        self.assertFalse(val)
        self.assertIn(
            f"File does not exist at {os.path.dirname(__file__)}",
            log.output[-1],
        )


class TestFind(unittest.TestCase):
    def call_func(
        self, path, filename, search_dirs=4, level="DEBUG"
    ) -> context.Tuple[str, str]:
        with self.assertLogs(level=level) as log:
            val = find_obj.find(path, filename, search_dirs)

        return log, val

    def test_found(self):
        log, val = self.call_func(os.path.dirname(__file__), "context.py")

        self.assertIsNotNone(val)

    def test_not_found(self):
        log, val = self.call_func(
            os.path.dirname(__file__), "hello.world", level="INFO"
        )

        self.assertIsNone(val)
        self.assertIn(
            "hello.world not found within 4 directories of "
            f"{os.path.dirname(__file__)}",
            log.output[-1],
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
