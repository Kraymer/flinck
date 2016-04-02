#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Flinck: Finger lickin good flicks linker.
"""

import argparse
import os
import sys

from . import confit
from . import brain

from .config import config
from .linker import Linker

__version__ = '0.2.0'
__author__ = 'Fabrice Laporte <kraymer@gmail.com>'


def parse_args(argv):
    """Build application argument parser and parse command line.
    """
    try:
        root_defined = config['link_root_dir'].get()
    except confit.NotFoundError:
        root_defined = False
    parser = argparse.ArgumentParser(
        description='Organize your movie collection using symbolic links')
    parser.add_argument('media_src',
                        metavar='FILE|DIR',
                        help='media file or directory')
    parser.add_argument('-l', '--link_dir',
                        help='links root directory',
                        dest='link_root_dir',
                        required=(not root_defined))
    parser.add_argument('--by',
                        choices=['country', 'director', 'decade',
                        'genre', 'rating', 'runtime', 'title', 'year'],
                        nargs='+',
                        metavar='FIELD1 FIELD2',
                        required=True,
                        help=('organize medias by...\n'
                              'Possible fields: {%(choices)s}'))
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + __version__,
                        help='display version information and exit')
    args = parser.parse_args(args=argv[1:])
    config.set_args(args)
    args = vars(args)
    try:
        args['media_src'] = unicode(args['media_src'], "utf-8",
                                    errors="ignore")
    except Exception:
        pass  # py3
    return args


def recursive_glob(treeroot, extensions):
    if not os.path.isdir(treeroot):
        yield treeroot
    for base, dirs, files in os.walk(treeroot):
        for f in files:
            if f.endswith(extensions):
                yield os.path.join(base, f)


def main(argv=None):
    args = parse_args(argv or sys.argv)
    if not args:
        exit(1)
    config_filename = os.path.join(config.config_dir(),
                                   confit.CONFIG_FILENAME)
    if not os.path.exists(config_filename):
        print(('Missing configuration file %s.' % config_filename))
    if not os.path.exists(config['link_root_dir'].as_filename()):
        print(('Error: links root directory "%s" does not exist.' %
              config['link_root_dir']))
        exit(1)
    linkers = [Linker(field) for field in args['by']]
    for f in recursive_glob(args['media_src'], ('.avi', '.mp4')):
        if os.path.getsize(f) < 20971520:
            continue
        item = brain.search_filename(f, args['by'])
        if item:
            for l in linkers:
                l.flink(item)
        else:
            print(('No imdb matching for %s' % f))

if __name__ == "__main__":
    sys.exit(main())
