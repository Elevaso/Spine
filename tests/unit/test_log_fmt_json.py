# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

# Python Standard Libraries
import context
from io import StringIO
import json
import logging.config
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
from common import setup_logger
from spine.log import append, fmt_json


class TestJsonLogging(unittest.TestCase):
    def setUp(self):
        self.buffer, self.logger, self.log_handler = setup_logger(
            logging.getLogger(__name__), "DEBUG"
        )

    def setFormat(self):
        formatter = fmt_json.JsonFormatter()
        self.log_handler.setFormatter(formatter)

    def get_config(self, timezone_name: str = "US/Central") -> dict:
        return {
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
                    "timezone": timezone_name,
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

    def test_invalid_tz(self):
        with self.assertRaises(ValueError) as cm:
            logging.config.dictConfig(self.get_config(timezone_name="hello"))

        self.assertEqual(
            str(cm.exception), "Unable to configure formatter 'json'"
        )

    def test_default_format(self):
        self.setFormat()

        msg = "testing logging format"
        self.logger.info(msg)
        log_json = json.loads(self.buffer.getvalue())

        self.assertEqual(log_json["message"], msg)

    # # This is an alternate way to perform the test, however, the logging
    # # messages will output in terminal since we're not trapping it via the
    # # buffer
    # def test_default_format(self):
    #     formatter = overcast.tools.json_logging.JsonFormatter()
    #     self.log_handler.setFormatter(formatter)

    #     msg = 'testing logging format'
    #     level = 'INFO'
    #     with self.assertLogs(level=level) as log:
    #         self.logger.info(msg)
    #         self.assertEqual(str(log.output),
    #         f'[\'{level}:{__name__}:{msg}\']')

    def test_extra(self):
        self.setFormat()

        msg = "testing logging format"
        self.logger.info(msg, extra={"test": "value"})
        log_json = json.loads(self.buffer.getvalue())

        self.assertEqual(log_json["test"], "value")

    def test_logging_config(self):
        config = self.get_config()

        self.buffer = StringIO()

        # Need to update the stream to StringIO otherwise the buffer won't
        # capture everything
        handler = config.get("handlers").get("console")
        handler.update({"stream": self.buffer})
        config.update({"handlers": {"console": handler}})

        logging.config.dictConfig(config)

        self.logger = append.LogAppend(
            self.logger, {"test": "value"}, adapter_priority=True
        )

        msg = "testing logging format"
        self.logger.info(msg, extra={"test": "newvalue"})
        log_json = json.loads(self.buffer.getvalue())

        self.assertEqual(log_json["test"], "value")
        self.assertEqual(log_json["message"], msg)

    def test_exc_info(self):
        self.setFormat()

        with self.assertLogs(level="WARN"):
            try:
                raise Exception("Test warning with exc_info")
            except Exception as e:
                self.logger.warning(str(e), exc_info=True)

        log_json = json.loads(self.buffer.getvalue())
        self.assertEqual(log_json["message"], "Test warning with exc_info")
        self.assertTrue("exc_info" in log_json)

    def test_dict(self):
        self.setFormat()

        msg = {"hello": "there"}
        self.logger.info(msg)
        log_json = json.loads(self.buffer.getvalue())

        self.assertEqual(log_json["hello"], "there")


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
