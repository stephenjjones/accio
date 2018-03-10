#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import codecs
from setuptools import setup

import accio

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

required = [
    'boto3=*',
    'clint=*'
]

setup(
    name='accio'
    version=accio.__version__,
    description='CLI for AWS resources',
    long_description=long_description,
    author='Stephen Jones',
    author_email='stephen.jacob.jones@gmail.com',
    url='https://github.com/stephenjjones/accio',
    packages= [
        'accio'
    ],
    install_requires=required,
    license='MIT',
    test_suite='test_accio',
    entry_points = {
        'console_scripts': ['accio=accio.cli:main']
    }
)
