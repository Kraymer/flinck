#!/usr/bin/env python

# Copyright (c) 2016 Fabrice Laporte - kray.me
# The MIT License http://www.opensource.org/licenses/mit-license.php

from setuptools import setup


def coerce_file(fn):
    """Coerce content of given file to something useful for setup(), turn :
       .py into mock object with description and version fields,
       .md into rst text. Remove images with "nopypi" alt text along the way.

       :url: https://github.com/Kraymer/setupgoon
    """
    import ast
    import os
    import re
    import subprocess  # noqa
    text = open(os.path.join(os.path.dirname(__file__), fn)).read()
    if fn.endswith('.py'):  # extract version, docstring etc out of python file
        mock = type('mock', (object,), {})()
        for attr in ('version', 'author', 'author_email', 'license'):
            regex = r'^__%s__\s*=\s*[\'"]([^\'"]*)[\'"]$' % attr
            m = re.search(regex, text, re.MULTILINE)
            setattr(mock, attr, m.group(1) if m else None)
        mock.docstring = ast.get_docstring(ast.parse(text))
        return mock
    if fn.endswith('md'):  # convert markdown to rest, filter out nopypi images
        text = '\n'.join([l for l in text.split('\n') if '![nopypi' not in l])
        p = subprocess.Popen(['pandoc', '-t', 'rst'], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        text, stderr = p.communicate(text)
    return text


setup(name='flinck',
      version=coerce_file('flinck/__init__.py').version,
      description=coerce_file('flinck/__init__.py').docstring,
      long_description=coerce_file('README.md'),
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
      install_requires=coerce_file('requirements.txt').split('\n'),
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Environment :: Console',
          'Topic :: System :: Filesystems',
          'Topic :: Multimedia :: Video'
      ],
      keywords="movies organization omdb symlinks",
      )
