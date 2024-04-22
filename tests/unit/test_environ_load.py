# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

# Python Standard Libraries
import context
import os
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
from spine.environ import load


class TestLoad(unittest.TestCase):
    def create_env_file(self, path: str = None, prefix: str = None):
        """Create an env file (required for CI/CD testing)

        Args:
            path (str, Optional): Defaults to current file path

            prefix (str, Optional): Prefix of filename
        """
        path = path or os.path.dirname(__file__)

        file_name = os.path.join(path, ".".join([prefix or "", "env"]))

        if os.path.exists(file_name):
            os.remove(file_name)  # pragma: no cover

        with open(file_name, "w+") as f:
            f.writelines(
                [
                    "TEST=hello\n",
                    "#TEST_COMMENT=Comment\n",
                    "TESTING=Partial value #with comment at the end\n",
                    "\n",
                    "INVALID\n",
                    "SPACE = TEST\n",
                    "EMPTY=",
                ]
            )

    def del_env_var(self, key: str):
        """Delete environment variable

        Args:
            key (str): Key to delete
        """
        if key in os.environ.keys():
            del os.environ[key]

    def cleanup(self, path: str = None, prefix: str = None):
        """Create an env file (required for CI/CD testing)

        Args:
            path (str, Optional): Defaults to current file path

            prefix (str, Optional): Prefix of filename
        """
        path = path or os.path.dirname(__file__)

        file_name = os.path.join(path, ".".join([prefix or "", "env"]))

        self.del_env_var("TEST")
        self.del_env_var("TESTING")
        self.del_env_var("SPACE")

        if os.path.exists(file_name):
            os.remove(file_name)  # pragma: no cover

    def test_default(self):
        path = None
        prefix = None

        self.create_env_file(path, prefix)

        load.load_env(path=os.path.dirname(__file__))

        try:
            self.assertEqual(os.environ.get("TEST"), "hello")

            self.assertEqual(os.environ.get("TESTING"), "Partial value")

            self.assertEqual(os.environ.get("SPACE"), "TEST")

            self.assertNotIn("INVALID", os.environ.keys())

            self.assertNotIn("TEST_COMMENT", os.environ.keys())

            self.assertNotIn("EMPTY", os.environ.keys())
        finally:
            self.cleanup(path, prefix)

    def test_no_file(self):
        with self.assertLogs(level="INFO") as log:
            load.load_env(search_dirs=2)

        self.assertIn(
            f".env not found within 2 directories of ",
            log.output[-1],
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
