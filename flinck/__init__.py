#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Flinck: Finger lickin good flicks linker.
"""

import argparse
import os
import sys

import brain

from config import config
from linker import Linker


def parse_args(argv):
    """Build application argument parser and parse command line.
    """
    parser = argparse.ArgumentParser(
        description='Organize your movie collection using symbolic links')
    parser.add_argument('media_src', metavar='FILE|DIR',
                        help='Media file or directory')
    parser.add_argument('-l', '--link_dir', help='Links directory')
    parser.add_argument('-f', '--full-dir-scan', action='store_true',
                        help='Link all files, not just the new ones')
    parser.add_argument('--by', choices=['country', 'director', 'decade',
                        'genre', 'rating', 'runtime', 'title', 'year'],
                        nargs='+',
                        required=True, help='Organize medias by...')
    args = parser.parse_args(args=argv[1:])
    config.set_args(args)
    return vars(args)


def recursive_glob(treeroot, extensions):
    if not os.path.isdir(treeroot):
        yield treeroot
    for base, dirs, files in os.walk(treeroot):
        for f in files:
            if f.endswith(extensions):
                yield os.path.join(base, f)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = parse_args(argv)
    if not args:
        exit(1)

    linkers = []
    for field in args['by']:
        linkers.append(Linker(field))
    for f in recursive_glob(args['media_src'], ('.avi', '.mp4')):
        item = brain.search_filename(f)
        if item:
            for l in linkers:
                l.flink(item)
        else:
            print 'No imdb matching for %s' % f

if __name__ == "__main__":
    sys.exit(main())
