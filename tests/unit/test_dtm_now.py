# pyright: reportMissingImports=false

# Python Standard Libraries
import datetime
import context
import unittest
import time

# 3rd Party Libraries


# Code Repository Sub-Packages
from spine.dtm import now  # pylint: disable=import-error


class TestUtcNow(unittest.TestCase):
    def test_basic(self):
        val = now.utc_now()

        self.assertIsInstance(val, datetime.datetime)
        self.assertEqual(val.tzinfo, datetime.timezone.utc)

        time.sleep(0.5)

        self.assertNotEqual(val, now.utc_now())


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
