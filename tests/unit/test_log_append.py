# pyright: reportMissingImports=false

# Python Standard Libraries
import context
import json
import logging
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
from common import setup_logger
from spine.log import append, fmt_json


class TestLogAppend(unittest.TestCase):
    def setUp(self):
        self.buffer, self.logger, self.log_handler = setup_logger(
            logging.getLogger(__name__), "DEBUG"
        )

    def setFormat(self):
        formatter = fmt_json.JsonFormatter()
        self.log_handler.setFormatter(formatter)

    def test_custom_adapter(self):
        self.setFormat()

        self.logger = append.LogAppend(self.logger, {"test": "value"})

        msg = "testing logging format"
        self.logger.info(msg)
        log_json = json.loads(self.buffer.getvalue())

        self.assertEqual(log_json["test"], "value")
        self.assertEqual(log_json["message"], msg)

        msg = "testing logging format again the test value should still exist"
        self.logger.info(msg)
        log_json = json.loads(self.buffer.getvalue().splitlines()[1])

        self.assertEqual(log_json["test"], "value")
        self.assertEqual(log_json["message"], msg)

    def test_custom_adapter_w_extra(self):
        self.setFormat()

        self.logger = append.LogAppend(self.logger, {"test": "value"})

        msg = "testing logging format"
        self.logger.info(msg, extra={"testing": "newvalue"})
        log_json = json.loads(self.buffer.getvalue())

        self.assertEqual(log_json["test"], "value")
        self.assertEqual(log_json["testing"], "newvalue")
        self.assertEqual(log_json["message"], msg)

    def test_collision_record_priority(self):
        self.setFormat()

        self.logger = append.LogAppend(self.logger, {"test": "value"})

        msg = "testing logging format"
        self.logger.info(msg, extra={"test": "newvalue"})
        log_json = json.loads(self.buffer.getvalue())

        self.assertEqual(log_json["test"], "newvalue")
        self.assertEqual(log_json["message"], msg)

    def test_collision_adapter_priority(self):
        self.setFormat()

        self.logger = append.LogAppend(
            self.logger, {"test": "value"}, adapter_priority=True
        )

        msg = "testing logging format"
        self.logger.info(msg, extra={"test": "newvalue"})
        log_json = json.loads(self.buffer.getvalue())

        self.assertEqual(log_json["test"], "value")
        self.assertEqual(log_json["message"], msg)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
