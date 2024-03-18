#!/usr/bin/env python

import os.path
from setuptools import setup, find_packages
import sys

ROOT = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(ROOT))

setup(
    package_dir={"": "src"},
    packages=find_packages(
        "src", exclude=["tests*", "scripts*", "docs*", "tools*"]
    ),
    include_package_data=True,
    zip_safe=True,
)
