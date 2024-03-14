"""
.. module:: find_obj
    :platform: Unix, Windows
    :synopsis: Find file object
"""

# Python Standard Libraries
import logging
import os

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


def find(path: str, file_name: str, search_dirs: int = 4) -> str:
    """Find a file by traversing the parent

    Args:
        file_path (str): Starting path

        file_name (str): Name of file to find

        search_dirs (int, Optional): Number of parent directories to traverse,
        defaults to 4

    Returns:
        str: Path of file found, None if file is not found
    """
    LOGGER.debug(f"Searching for {file_name} in {path}")

    file_path = path

    for _ in range(0, search_dirs):
        if os.path.exists(os.path.join(file_path, file_name)):
            return file_path
        else:
            file_path = os.path.join(file_path, "..")

    LOGGER.info(
        f"{file_name} not found within {search_dirs} directories of {path}"
    )

    return None
