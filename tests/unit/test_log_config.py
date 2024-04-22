# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Python Standard Libraries
import context
from io import StringIO
import json
import logging
import os
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
from common import setup_logger
from spine.log import config


class TestSetup(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.buffer = StringIO()
        self.config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "include_keys": [
                        "message",
                        "module",
                        "levelname",
                        "name",
                        "funcName",
                        "asctime",
                        "thread",
                        "threadName",
                    ],
                    "()": "spine.log.fmt_json.JsonFormatter",
                    "timestamp_key": "timestamp",
                    "session_key": "init_id",
                    "timezone": "US/Central",
                    "dtm_format": "%Y-%m-%d %H:%M:%S %Z",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "json",
                    "stream": self.buffer,
                }
            },
            "root": {
                "level": "INFO",
                "handlers": ["console"],
                "propogate": "no",
            },
        }

    def test_invalid_log_format(self):
        with self.assertRaises(ValueError) as cm:
            config.setup(log_format="hello")

        self.assertEqual(
            str(cm.exception), "Invalid log_format specified: hello"
        )

    def test_default_config(self):
        config.setup(log_format="json")

    def test_default_config_overwrite_level(self):
        config.setup(log_format="json", log_level="WARNING")

    # TODO Add test case once common items are added SPIN-25
    # def test_append_common(self):
    #     os.environ["AWS_REGION"] = "test-us"

    #     config.setup(log_config=self.config)

    #     msg = "testing logging format"
    #     self.logger.info(msg, extra={"hello": "there"})
    #     log_json = json.loads(self.buffer.getvalue())

    #     self.assertEqual(log_json["aws_region"], "test-us")
    #     self.assertEqual(log_json["message"], msg)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
