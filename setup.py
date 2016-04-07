#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Fabrice Laporte - kray.me
# The MIT License http://www.opensource.org/licenses/mit-license.php

import os
import re

from setuptools import setup


def yield_sphinx_only_markup(lines):
    """http://stackoverflow.com/a/25900928/5181
       Cleans-up Sphinx-only constructs (ie from README.rst),
       so that *PyPi* can format it properly.
       To check for remaining errors, install ``sphinx`` and run::
       python setup.py --long-description | sed -file 'this_file.sed' | rst2html.py  --halt=warning

    """
    substs = [
        # Selected Sphinx-only Roles.
        (r':abbr:`([^`]+)`', r'\1'),
        (r':ref:`([^`]+)`', r'`\1`_'),
        (r':term:`([^`]+)`', r'**\1**'),
        (r':dfn:`([^`]+)`', r'**\1**'),
        (r':(samp|guilabel|menuselection):`([^`]+)`', r'``\2``'),

        # Sphinx-only roles:
        (r':(\w+):`([^`]*)`', r'\1(``\2``)'),

        # Sphinx-only Directives.
        (r'\.\. doctest', r'code-block'),
        (r'\.\. plot::', r'.. '),
        (r'\.\. seealso', r'info'),
        (r'\.\. glossary', r'rubric'),
        (r'\.\. figure::', r'.. '),

        # Other
        (r'\|version\|', r'x.x.x'),
    ]

    regex_subs = [(re.compile(regex, re.IGNORECASE), sub)
                  for (regex, sub) in substs]

    def clean_line(line):
        try:
            for (regex, sub) in regex_subs:
                line = regex.sub(sub, line)
        except Exception as ex:
            print(("ERROR: %s, (line(%s)" % (regex, sub)))
            raise ex
        return line

    for line in lines:
        yield clean_line(line)


def version():
    path = os.path.join(os.path.dirname(__file__), 'flinck', '__init__.py')
    with open(path) as f:
        for line in f:
            tokens = line.split('__version__ = ')
            if len(tokens) > 1:
                return tokens[1].strip("' \n")
        else:
            print('No version defined')
            exit(1)


readme_lines = open('README.rst').readlines()
setup(name='flinck',
    version=version(),
    description='Sort your movies on filesystem using symlinks.',
    long_description=''.join(yield_sphinx_only_markup(readme_lines)),
    author='Fabrice Laporte',
    author_email='kraymer@gmail.com',
    url='https://github.com/KraYmer/flinck',
    license='MIT',
    platforms='ALL',
    packages=['flinck', ],

    entry_points={
        'console_scripts': [
            'flinck = flinck:main',
        ],
    },
    install_requires=['omdb',
        'unidecode',
        'pyyaml'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Environment :: Console',
        'Topic :: System :: Filesystems',
        'Topic :: Multimedia :: Video'
    ]
)
