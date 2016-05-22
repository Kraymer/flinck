#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Flinck: Finger lickin good flicks linker.
"""

from __future__ import print_function

import logging
import os
import sys

import click

from . import confit
from . import brain

from .config import config, FIELDS
from .linker import Linker
from .version import __version__

__author__ = 'Fabrice Laporte <kraymer@gmail.com>'



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


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('media_src', type=click.Path(exists=True), metavar='FILE|DIR')
@click.option('--link_dir', '-l', type=click.Path(exists=True),
    required=(not config['link_root_dir']),
    default=os.path.expanduser(config['link_root_dir'].get()),
    help='Links root directory')
@click.option('--by', '-b', multiple=True, type=click.Choice(FIELDS),
    required=(not set(config.keys()).intersection(FIELDS)),
    help='Organize medias by...')
@click.option('-v', '--verbose', count=True)
@click.version_option(__version__)
def flinck(media_src, link_dir, by, verbose):
    if link_dir:
        config['link_root_dir'] = link_dir
    if not config['link_root_dir'] or not \
            os.path.exists(config['link_root_dir'].as_filename()):
        print('Error: links root directory "%s" does not exist.' %
              config['link_root_dir'])
        exit(1)
    linkers = [Linker(field) for field in by]
    for fpath in recursive_glob(media_src):
        item = brain.search_filename(fpath, by, verbose=verbose)
        if item:
            for linker in linkers:
                linker.flink(item, verbose=verbose)
            if verbose:
                print('Done: %s' % os.path.basename(fpath))
        else:
            print('Error: %s: no result in Open Movie Database' %
                os.path.basename(fpath))


if __name__ == "__main__":
    flinck()
