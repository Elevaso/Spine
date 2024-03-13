"""
.. module:: context
    :platform: Unix, Windows
    :synopsis: File for all test scripts to reference back to the main toolkit library
"""

# Python Standard Libraries
import os
import sys
from typing import Tuple, Union

# 3rd Party Libraries


# Code Repository Sub-Packages


sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "src")
    ),
)

