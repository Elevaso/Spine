"""
.. module:: common
    :platform: Unix, Windows
    :synopsis: Common functions/classes used by multiple tests
"""
# pylint: disable=missing-class-docstring, missing-function-docstring

# Python Standard Libraries
from io import StringIO
import logging
from typing import Tuple

# 3rd Party Libraries


# Code Repository Sub-Packages


def rm_log_handlers(logger: logging.Logger):
    for i in logger.handlers:
        logger.removeHandler(i)


def disable_root_logger():
    logger = logging.getLogger().root

    rm_log_handlers(logger)


def setup_logger(
    logger: logging.Logger, level_name: str, rm_handlers: bool = True
) -> Tuple[StringIO, logging.Logger, object]:
    logger.setLevel(logging.getLevelName(level_name))
    buffer = StringIO()

    disable_root_logger()

    if rm_handlers:
        rm_log_handlers(logger)

    log_handler = logging.StreamHandler(buffer)
    logger.addHandler(log_handler)

    return buffer, logger, log_handler
