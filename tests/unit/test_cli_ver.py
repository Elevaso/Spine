# pyright: reportMissingImports=false

# Python Standard Libraries
import context
import argparse
from io import StringIO
import unittest
from unittest import mock

# 3rd Party Libraries


# Code Repository Sub-Packages
from spine.cli import ver


class TestAddVersion(unittest.TestCase):
    def call_func(
        self, parser_obj: argparse.ArgumentParser, version: object = None
    ):
        ver.add_version(parser_obj, version)

    def test_no_version(self):
        output = StringIO()
        parser_obj = argparse.ArgumentParser()

        with self.assertLogs(level="DEBUG") as log:
            self.call_func(parser_obj, None)

        self.assertEqual(
            log.output[0].split(":")[-1], "No version provided, skipping"
        )

    @mock.patch("sys.argv", [__file__, "--version"])
    def test_version(self):
        output = StringIO()
        parser_obj = argparse.ArgumentParser()

        self.call_func(parser_obj, "1.0.0")

        with self.assertRaises(SystemExit) as cm:
            with mock.patch("sys.stdout", new=output):
                _ = parser_obj.parse_args()

        self.assertEqual(str(cm.exception), "0")
        self.assertEqual(output.getvalue(), "1.0.0\n")


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
