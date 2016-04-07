#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Flinck: Finger lickin good flicks linker.
"""

from __future__ import print_function

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
        description='Organize your movie collection using symbolic links',
        epilog='Example: flinck ~/Movies --by genre rating',)
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
    except NameError:
        pass  # Python3, no conversion needed
    return args


def recursive_glob(treeroot):
    """Browse folders hierarchy and yield files with
    """
    min_size = config['file_min_size_mb'].get() * 1024 * 1024

    def is_video_file_candidate(path):
        return (path.endswith(tuple(config['file_extensions'].get())) and
                os.path.getsize(path) > min_size)

    if not os.path.isdir(treeroot) and is_video_file_candidate(treeroot):
        yield treeroot
    for base, _, files in os.walk(treeroot):
        for fpath in files:
            abs_path = os.path.join(base, fpath)
            if is_video_file_candidate(abs_path):
                yield abs_path


def main(argv=None):
    args = parse_args(argv or sys.argv)
    if not args:
        exit(1)
    config_filename = os.path.join(config.config_dir(),
                                   confit.CONFIG_FILENAME)
    if not os.path.exists(config_filename):
        print('Missing configuration file %s.' % config_filename)
    if not os.path.exists(config['link_root_dir'].as_filename()):
        print('Error: links root directory "%s" does not exist.' %
              config['link_root_dir'])
        exit(1)
    linkers = [Linker(field) for field in args['by']]
    for fpath in recursive_glob(args['media_src']):
        item = brain.search_filename(fpath, args['by'])
        if item:
            for linker in linkers:
                linker.flink(item)
        else:
            print('No Open Movie Database matching for %s' % fpath)

if __name__ == "__main__":
    sys.exit(main())
