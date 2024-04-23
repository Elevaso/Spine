# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Python Standard Libraries
import json
import os
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
import context  # pylint: disable=unused-import
from spine.cli import setup


class TestBuildArgparse(unittest.TestCase):
    def test_none(self):
        with self.assertRaises(AttributeError) as exce:
            _ = setup.build()

        self.assertEqual(
            str(exce.exception), "Valid path or arg_dict value must be provided"
        )

    def test_invalid_type(self):
        with self.assertRaises(TypeError) as exce:
            _ = setup.build(arg_dict=["hello"])

        self.assertEqual(
            str(exce.exception),
            "Invalid type of <class 'list'> for path content or"
            " arg_dict value",
        )

    def test_path(self):
        parser = setup.build(
            path=os.path.join(
                os.path.dirname(__file__), "..", "samples", "argparse.json"
            )
        )

        self.assertEqual(parser.description, "Test CLI Description")

        self.assertEqual("quiet", parser.__dict__["_actions"][2].dest)

    def test_arg_dict(self):
        with open(
            os.path.join(
                os.path.dirname(__file__), "..", "samples", "argparse.json"
            ),
            "r",
        ) as file:
            parser = setup.build(arg_dict=json.loads(file.read()))

        self.assertEqual(parser.description, "Test CLI Description")

        self.assertEqual("quiet", parser.__dict__["_actions"][2].dest)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
