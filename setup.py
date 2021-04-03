#!/usr/bin/env python
#
# Copyright (c) 2021 Carsten Igel.
#
# This file is part of iteratedc
# (see https://github.com/carstencodes/iteratedc).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

from setuptools import setup, find_packages

__VERSION__ = "0.6.5"

long_description: str = ""
with open("README.md", "r") as read_me_file:
    long_description = read_me_file.read()

setup(
    name="iteratedc",
    version=__VERSION__,
    license="BSD 3-Clause",
    author="Carsten Igel",
    author_email="cig@bite-that-bit.de",
    description="Iterator for data classes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    url="https://github.com/carstencodes/iteratedc",
    install_requires=[],
    package_dir={"": "src"},
    keywords="",
    python_requires=">=3.8, < 4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System",
        "Typing :: Typed",
    ],
)
