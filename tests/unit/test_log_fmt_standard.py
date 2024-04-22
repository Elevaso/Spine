# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

# Python Standard Libraries
import context
import logging.config
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
from common import setup_logger
from spine.log import fmt_standard


class TestStandardLogging(unittest.TestCase):
    def setUp(self):
        self.buffer, self.logger, self.log_handler = setup_logger(
            logging.getLogger(__name__), "DEBUG"
        )

    def setFormat(self, include_extra: bool = False, format: str = None):
        formatter = fmt_standard.StandardFormatter(
            include_extra=include_extra, format=format
        )
        self.log_handler.setFormatter(formatter)

    def get_config(self, timezone_name: str = "US/Central") -> dict:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "()": "spine.log.fmt_standard.StandardFormatter",
                    "format": "[${levelname}]",
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
                    "formatter": "standard",
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
            str(cm.exception), "Unable to configure formatter 'standard'"
        )

    def test_default_format(self):
        self.setFormat()

        msg = "testing logging format"
        self.logger.info(msg)
        log = self.buffer.getvalue().strip()

        self.assertEqual(log, msg)

    def test_extra_without_including(self):
        self.setFormat()

        msg = "testing logging format"
        self.logger.info(msg, extra={"test": "value"})
        log = self.buffer.getvalue().strip()

        self.assertEqual(log, msg)

    def test_extra(self):
        self.setFormat(include_extra=True)

        msg = "testing logging format"
        extra_vals = {"test": "value"}
        self.logger.info(msg, extra=extra_vals)
        log = self.buffer.getvalue().strip()

        self.assertEqual(
            log,
            msg
            + " || Extra || "
            + "..".join([f"[{k} || {v}]" for k, v in extra_vals.items()]),
        )

    def test_custom_format(self):
        self.setFormat(format="%(levelname)s")

        msg = "testing logging format"
        extra_vals = {"test": "value"}
        self.logger.info(msg, extra=extra_vals)
        log = self.buffer.getvalue().strip()

        self.assertEqual(log, "INFO")

    def test_custom_format_w_extra(self):
        self.setFormat(format="%(levelname)s", include_extra=True)

        msg = "testing logging format"
        extra_vals = {"test": "value"}
        self.logger.info(msg, extra=extra_vals)
        log = self.buffer.getvalue().strip()

        self.assertEqual(
            log,
            "INFO || Extra || "
            + "..".join([f"[{k} || {v}]" for k, v in extra_vals.items()]),
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
