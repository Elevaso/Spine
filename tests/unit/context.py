"""
.. module:: context
    :platform: Unix, Windows
    :synopsis: File for all test scripts to reference back to the main
    toolkit library
"""
# pylint: disable=missing-class-docstring, missing-function-docstring

# Python Standard Libraries
import os
import sys
from typing import Tuple  # pylint: disable=unused-import

# 3rd Party Libraries


# Code Repository Sub-Packages


sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "src")
    ),
)
