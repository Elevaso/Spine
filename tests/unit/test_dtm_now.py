# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Python Standard Libraries
import datetime
import unittest
import time

# 3rd Party Libraries


# Code Repository Sub-Packages
import context  # pylint: disable=unused-import
from spine.dtm import now


class TestUtcNow(unittest.TestCase):
    def test_basic(self):
        val = now.utc_now()

        self.assertIsInstance(val, datetime.datetime)
        self.assertEqual(val.tzinfo, datetime.timezone.utc)

        time.sleep(0.5)

        self.assertNotEqual(val, now.utc_now())


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
