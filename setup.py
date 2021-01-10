#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


def get_version() -> str:
    with open("transip/__init__.py") as file:
        for line in file:
            if line.startswith("__version__"):
                return line.replace("\"", "").split()[-1]


def get_long_description() -> str:
    with open("README.md", "r") as file:
        return file.read()


setup(
    name="python-transip",
    version=get_version(),
    description="Wrapper for the TransIP API",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Roald Nefs",
    author_email="info@roaldnefs.com",
    license="LGPLv3",
    url="https://github.com/roaldnefs/python-transip",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["cryptography>=3.3.1", "requests>=2.25.1"],
    python_requires=">=3.6.12",
    entry_points={},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    extras_require={},
)
