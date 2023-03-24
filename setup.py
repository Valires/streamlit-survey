#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "streamlit"
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Olivier Binette",
    author_email="olivier.binette@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 (AGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Survey components for Streamlit apps",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="streamlit_survey",
    name="streamlit_survey",
    packages=find_packages(include=["streamlit_survey", "streamlit_survey.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/OlivierBinette/streamlit_survey",
    version="0.1.0",
    zip_safe=False,
)
