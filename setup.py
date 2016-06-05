#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Fabrice Laporte - kray.me
# The MIT License http://www.opensource.org/licenses/mit-license.php

from setuptools import setup

import setupgoon as goon

setup(name='flinck',
    version=goon.get('flinck/__init__.py').version,
    description=goon.get('flinck/__init__.py').docstring,
    long_description=goon.get('README.rst').text,
    author='Fabrice Laporte',
    author_email='kraymer@gmail.com',
    url='https://github.com/KraYmer/flinck',
    license='MIT',
    platforms='ALL',
    packages=['flinck', ],

    entry_points={
        'console_scripts': [
            'flinck = flinck:flinck_cli',
        ],
    },
    install_requires=['click',
        'omdb',
        'pyyaml'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Environment :: Console',
        'Topic :: System :: Filesystems',
        'Topic :: Multimedia :: Video'
    ],
    keywords="movies organization omdb symlinks",
)
