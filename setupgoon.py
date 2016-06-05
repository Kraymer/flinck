#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Fabrice Laporte - kray.me
# The MIT License http://www.opensource.org/licenses/mit-license.php

"""setupgoon extorts information from package raw files so that setup.py can
   stay clean.
"""

import ast
import io
import re
from collections import namedtuple

PyInfo = namedtuple('PyInfo', 'version docstring')
RstInfo = namedtuple('RstInfo', 'text')
FILE_INFO = {}
SUBSTS = [
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
    (r'\|$', '|  '),
]


def as_pypi_rst(text):
    """Return rst file content after edition so that *PyPi* can format it
       properly.
    """
    def count_indent(line):
        return len(line) - len(line.lstrip())

    regex_subs = [(re.compile(regex, re.IGNORECASE), sub)
                  for (regex, sub) in SUBSTS]
    out_lines = []
    skip, skip_indent = False, -1
    for line in text.split('\n'):
        # Strip blocks introduced by a nopypi comment
        if line.lstrip().startswith('.. nopypi'):
            skip, skip_indent = True, count_indent(line)
            continue
        if skip:
            skip = False
            continue
        elif skip_indent > -1:
            if count_indent(line) > skip_indent:
                continue
            else:
                skip_indent = -1
        # Replace unrecognized sphinx keywords
        for (regex, sub) in regex_subs:
            line = regex.sub(sub, line)
        out_lines.append(line)

    return '\n'.join(out_lines)


def version(text):
    """Return __version__ value.
    """
    regex = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]$'
    return re.search(regex, text, re.MULTILINE).group(1)


def docstring(text):
    """Return module docstring.
    """
    return ast.get_docstring(ast.parse(text))


def get(filename, cache=True):
    """Return a named tuple representing information extracted from file.
    """
    if not cache or filename not in FILE_INFO:
        with io.open(filename, 'r') as f:
            text = f.read()
            if filename.endswith('.py'):
                FILE_INFO[filename] = PyInfo(version(text), docstring(text))
            elif filename.endswith('.rst'):
                FILE_INFO[filename] = RstInfo(as_pypi_rst(text))
    return FILE_INFO[filename]
