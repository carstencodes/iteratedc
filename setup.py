#!/usr/bin/env python

from setuptools import setup, find_packages

__VERSION__ = "0.1.0"

long_description: str = ""
with open("README.md", "r") as read_me_file:
    long_description = read_me_file.read()

setup(
    name="###NAME###",
    version=__VERSION__,
    license="###LIC###",
    author="Carsten Igel",
    author_email="cig@bite-that-bit.de",
    description="###DESCRIPTION###",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    url="https://github.com/carstencodes/###REPO###",
    install_requires=[],
    package_dir={"": "src"},
    keywords="",
    python_requires=">=3.7, < 4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System",
        "Typing :: Typed",
    ],
)
