# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Python Standard Libraries
import logging
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
import context  # pylint: disable=unused-import
from common import setup_logger
from spine.log import fmt


class TestBaseFormatter(unittest.TestCase):
    def setUp(self):
        self.buffer, self.logger, self.log_handler = setup_logger(
            logging.getLogger(__name__), "DEBUG"
        )

    def setFormat(self, format: str = None):
        formatter = fmt.BaseFormatter(format=format)
        self.log_handler.setFormatter(formatter)

    def test_no_format(self):
        self.setFormat()

        msg = "testing logging format"
        self.logger.info(msg)
        log_val = self.buffer.getvalue().strip()

        self.assertEqual(log_val, msg)

    def test_format(self):
        self.setFormat(format="%(levelname)s %(message)s")

        msg = "testing logging format"
        self.logger.info(msg)
        log_val = self.buffer.getvalue().strip()

        self.assertEqual(log_val, "INFO " + msg)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
