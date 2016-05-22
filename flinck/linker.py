#!/usr/bin/python

"""Linkers are in charge of creating symlinks for one of the tree branches.
"""

from __future__ import print_function

import logging
import re
import os
from glob import glob

from .config import config

logger = logging.getLogger(__name__)


def resolve_template(template, item):
    """Resolve template pattern, replacing placeholders by item values.
    """
    root_dir = config['link_root_dir'].as_filename()
    placeholders = re.findall(r'(\%\{?\w+\}?)', template)
    path = template
    for p in placeholders:
        path = path.replace(p, item[p.strip('%{}')])
    return os.path.join(root_dir, path)


def create_dir(link_dir):
    """A os.makedirs that doesn't throw.
    """
    if not os.path.exists(link_dir):
        os.makedirs(link_dir)


def dircmp(val, link_dir):
    """Return a positive distance if link_dir matches val or -1 if no match.
    """
    is_range = (link_dir[0] == '[') and (link_dir[-1] == ']'
                                         ) and link_dir.count('-') == 1
    link_dir = link_dir.strip('[]')
    if val.startswith(link_dir):
        return 0
    elif link_dir.endswith('+'):
        if val > link_dir[:-1]:
            return 1.0 / len(link_dir)
    elif is_range:
        _min, _max = link_dir.split('-')
        length = len(_min)
        if _min <= val[:length] <= _max:
            return 0
    return -1


def find_bucket(parent_dir, val):
    """Find a sub directory of parent_dir whose name is compatible with val.

       It occurs if val starts with folder name or if val belongs to folder
       name implied range.
    """
    candidates = glob(parent_dir + '/*/')
    bucket = None
    min_distance = 99
    for c in sorted([os.path.basename(c.strip(os.path.sep))
                    for c in candidates], key=lambda x: x.strip('[]').lower()):
        distance = dircmp(val.lower(), c.lower())
        if 0 <= distance <= min_distance:
            bucket = c
            min_distance = distance

    if not bucket:
        logger.warning("Found no folder defining a compatible "
            "range for '%s'" % val)
    return bucket


class Linker():
    def __init__(self, name):
        self.field = name
        self.config = config[name]
        self.config.add({'root': self.field,
                        'dirs': False,
                        'buckets': False})
        self.root = self.config['root'].get()
        self.dirs = self.config['dirs'].get()
        self.buckets = self.config['buckets'].get()
        default_link_format = '%s%s%s' % (
            ('%%%s' % self.field) if not self.dirs else '',
            '-' if (not self.dirs and self.field != 'title') else '',
            '%title' if self.field != 'title' else '')
        self.config.add({'link_format': default_link_format})
        self.link_format = self.config['link_format'].get()

    def flink(self, item, verbose):
        link_path = resolve_template(os.path.join(self.root,
                                     self.link_format), item)
        link_dir, link_name = os.path.split(link_path)
        last_dir = ''
        if self.dirs:
            last_dir = item[self.field]
        if self.buckets:
            bucket = find_bucket(link_dir, item[self.field])
            if bucket and bucket != last_dir:
                last_dir = os.path.join(bucket , last_dir)
        if last_dir:
            link_dir = os.path.join(link_dir, last_dir)
        create_dir(link_dir)
        dest = os.path.join(link_dir, link_name)
        if not os.path.lexists(dest):
            logger.debug('Linking %s' % dest)
            os.symlink(item['filename'], dest)
        else:
            logger.warning('%s already exist' % dest)

