# pyright: reportMissingImports=false

# Python Standard Libraries
import context
import os
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
from spine.fobj import find_obj


class TestFind(unittest.TestCase):
    def call_func(
        self, path, filename, search_dirs=4
    ) -> context.Tuple[str, str]:
        with self.assertLogs(level="DEBUG") as log:
            val = find_obj.find(path, filename, search_dirs)

        return log, val

    def test_found(self):
        log, val = self.call_func(os.path.dirname(__file__), "context.py")

        self.assertIsNotNone(val)

    def test_not_found(self):
        log, val = self.call_func(os.path.dirname(__file__), "hello.world")

        self.assertIsNone(val)
        self.assertIn(
            f"hello.world not found within 4 directories of {os.path.dirname(__file__)}",
            log.output[-1],
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
