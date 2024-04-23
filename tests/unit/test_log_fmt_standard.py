# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Python Standard Libraries
import logging.config
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
import context  # pylint: disable=unused-import
from common import setup_logger
from spine.log import fmt_standard


class TestStandardLogging(unittest.TestCase):
    def setUp(self):
        self.buffer, self.logger, self.log_handler = setup_logger(
            logging.getLogger(__name__), "DEBUG"
        )

    def set_format(self, include_extra: bool = False, fmt: str = None):
        formatter = fmt_standard.StandardFormatter(
            include_extra=include_extra, format=fmt
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
        with self.assertRaises(ValueError) as exce:
            logging.config.dictConfig(self.get_config(timezone_name="hello"))

        self.assertEqual(
            str(exce.exception), "Unable to configure formatter 'standard'"
        )

    def test_default_format(self):
        self.set_format()

        msg = "testing logging format"
        self.logger.info(msg)
        log = self.buffer.getvalue().strip()

        self.assertEqual(log, msg)

    def test_extra_without_including(self):
        self.set_format()

        msg = "testing logging format"
        self.logger.info(msg, extra={"test": "value"})
        log = self.buffer.getvalue().strip()

        self.assertEqual(log, msg)

    def test_extra(self):
        self.set_format(include_extra=True)

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
        self.set_format(fmt="%(levelname)s")

        msg = "testing logging format"
        extra_vals = {"test": "value"}
        self.logger.info(msg, extra=extra_vals)
        log = self.buffer.getvalue().strip()

        self.assertEqual(log, "INFO")

    def test_custom_format_w_extra(self):
        self.set_format(fmt="%(levelname)s", include_extra=True)

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
