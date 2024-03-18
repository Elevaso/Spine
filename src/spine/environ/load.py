"""
.. module:: load
    :platform: Unix, Windows
    :synopsis: Load environment variables into memory/session
"""

# Python Standard Libraries
import logging
import os
import re
from typing import Tuple

# 3rd Party Libraries


# Project Specific Libraries
from spine.app import caller
from spine.environ import var
from spine.fobj import find_obj

LOGGER = logging.getLogger(__name__)

KEY_VALUE_REGEX = re.compile(r"^(?P<key>[\w\d]+)\s*=\s*(?P<value>[^#]+)")


def load_env(
    prefix: str = None,
    path: str = None,
    overwrite: bool = False,
    search_dirs: int = 4,
):
    """Load a .env file into Environment Variables

    Args:
        prefix (str, Optional): Prefix of the file, defaults to None

        .. note::
            Useful if you want to have a dev.env, test.env, prod.env setup

        path (str, Optional): Base path to start searching for env files,
        defaults to None

        .. note::
            If None, then will lookup the calling python functions path

        overwrite (bool, Optional): True/False if existing environment
        variables should be overwritten by .env file content, defaults to False

        search_dirs (int, Optional): Number of parent directories to traverse,
        defaults to 4
    """
    if not path:
        _, path = caller.get_caller()

    file_name = ".".join([prefix or "", "env"])

    env_content = None

    file_path = find_obj.find(path, file_name, search_dirs)

    if file_path:
        with open(os.path.join(file_path, file_name), "r") as f:
            env_content = f.read() or ""

        for e, i in enumerate(env_content.split("\n")):
            __check(i, e, set_val=True, overwrite=overwrite)


def __check(
    content: str,
    line_num: int = None,
    set_val: bool = True,
    overwrite: bool = False,
) -> bool:
    """Check if environment variable should be set

    Args:
        content (str): String in <ENV>=<VAL> format

        line_num (int, Optional): Line number (if processing from file)

        set_val (bool, Optional): True/False to execute the set_env_var
        function if content is valid

        overwrite (bool, Optional): True/False if existing environment
        variables should be overwritten by .env file content, defaults
        to False

    Returns:
        bool: True/False if set
    """
    return_val = False
    line_num_text = f"Line number {line_num}" if line_num else "Content"

    content = content.strip()

    if __valid(content, line_num_text):
        key, value = split_key_val(content)

        if key and value:
            return_val = var.set(key, value, overwrite, set_val)
        else:
            LOGGER.debug(
                f"{line_num_text} does not match [\\w\\d]=[^#], skipping"
            )

    return return_val


def __valid(content: str, line_num_text: str) -> bool:
    """Checks if the content is valid for continuing

    Args:
        content (str): String in <ENV>=<VAL> format

        line_num_text (str): Text to display in logging

    Returns:
        bool: True/False if content is valid for continuing
    """
    if content is None:
        LOGGER.debug(f"{line_num_text} is empty, skipping")  # pragma: no cover
    elif len(content) == 0:
        LOGGER.debug(f"{line_num_text} is blank, skipping")
    elif content[0] == "#":
        LOGGER.debug(f"{line_num_text} is comment, skipping")
    else:
        return True

    return False


# TODO Move this to anvil for ANV-3
def split_key_val(
    content: str, pattern: re.Pattern = KEY_VALUE_REGEX
) -> Tuple[str, str]:
    """Function to split a string into Key/Value pair

    Args:
        content (str): String to split

        pattern (re.Pattern, Optional): Regular Expression Pattern for
        splitting string, defaults to KEY=VAL expression

    Returns:
        str, str: Tuple of Key and Value
    """
    if pattern.match(content):
        match_set = pattern.match(content)

        return match_set.group("key").strip(), match_set.group("value").strip()
    else:
        return None, None
