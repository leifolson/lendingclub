"""
setup.py
Copyright (C) 2017 Clinton Olson (clint.olson2@gmail.com) and contributors

This module is part of lendingclub and is released under
the MIT License: https://opensource.org/licenses/MIT
"""


# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='lendingclub',
    version='0.1.0',
    description='A lightweight API to Lending Club',
    long_description=readme,
    author='Clinton Olson',
    author_email='clint.olson2@gmail.com',
    url='https://github.com/leifolson/lendingclub',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
