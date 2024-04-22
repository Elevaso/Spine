# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Python Standard Libraries
from io import StringIO
import os
import unittest
from unittest import mock

# 3rd Party Libraries


# Code Repository Sub-Packages
import context  # pylint: disable=unused-import
from spine.cli import exc


def mock_list_config(**kwargs):
    print(kwargs)


DEFAULT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "samples", "argparse.json"
)

DEFAULT_FUNC_MAP = {"list_config": mock_list_config}

BASIC_ARGS = [__file__, "config", "list"]


class TestArgsToDict(unittest.TestCase):
    def list_config(self, **kwargs):
        print(kwargs)

    def basic_call(self, path: str, func_map: object):
        with mock.patch("sys.stdout", new=StringIO()):
            exc.main(
                config_path=path,
                func_map=func_map,
                cli_version="0.1.0",
            )

    @mock.patch("sys.argv", BASIC_ARGS)
    def test_basic_setup(self):
        self.basic_call(DEFAULT_PATH, DEFAULT_FUNC_MAP)

    @mock.patch("sys.argv", [__file__, "--quiet"])
    def test_quiet(self):
        self.basic_call(DEFAULT_PATH, DEFAULT_FUNC_MAP)

    @mock.patch("sys.argv", [__file__, "--verbose"])
    def test_verbose(self):
        self.basic_call(DEFAULT_PATH, DEFAULT_FUNC_MAP)

    @mock.patch("sys.argv", BASIC_ARGS)
    def test_config_not_found(self):
        with self.assertRaises(FileNotFoundError) as cm:
            exc.main(
                config_path="hello.txt",
                func_map=DEFAULT_FUNC_MAP,
                cli_version="0.1.0",
            )

        self.assertEqual(
            str(cm.exception), "Arg config path hello.txt not found"
        )

    @mock.patch("sys.argv", [__file__, "config", "show"])
    def test_no_exec_func(self):
        with mock.patch("sys.stdout", new=StringIO()):
            exc.main(
                config_path=DEFAULT_PATH,
                func_map=DEFAULT_FUNC_MAP,
                cli_version="0.1.0",
            )

    @mock.patch("sys.argv", BASIC_ARGS)
    def test_func_map_lib(self):
        self.basic_call(DEFAULT_PATH, self)

    @mock.patch("sys.argv", BASIC_ARGS)
    def test_exec_func_not_found(self):
        with self.assertRaises(AttributeError) as cm:
            with self.assertLogs(level="INFO") as log:
                with mock.patch("sys.stdout", new=StringIO()):
                    exc.main(
                        config_path=DEFAULT_PATH,
                        func_map={},
                        cli_version="0.1.0",
                    )

        self.assertEqual(
            str(cm.exception), "Command/Function list_config not found"
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
