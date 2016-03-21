#!/usr/bin/python

"""Linkers are in charge of creating symlinks for one of the tree branches.
"""

import re
import os

from glob import glob

from config import config


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


def belongs_to(val, link_dir):
    """Return True if val belongs to the range defined by link_dir.
    """
    if link_dir.endswith('-'):
        return val < link_dir[:-1]
    elif link_dir.endswith('+'):
        return val > link_dir[:-1]
    elif link_dir[1:-1].count('-') == 1:
        _min, _max = link_dir.split('-')
        return _min <= val < _max


def find_bucket(parent_dir, val):
    """Find a sub directory of parent_dir whose name is compatible with val.

       It occurs if val starts with folder name or if val belongs to folder
       name implied range.
    """
    candidates = glob(parent_dir + '/*/')
    for c in [os.path.normpath(c) for c in candidates]:
        if val.startswith(c):
            return c
        if (c[0] in '][' and c[-1] in '][') and belongs_to(val, c[1:-1]):
            return c


class Linker():
    def __init__(self, name):
        self.field = name
        self.config = config[name]
        self.config.add({'link_rel_dir': self.field,
                        'dirs': False,
                        'buckets': False})
        self.link_rel_dir = self.config['link_rel_dir'].get()
        self.dirs = self.config['dirs'].get()
        self.buckets = self.config['buckets'].get()
        default_link_format = '%s%s%s' % (
            ('%%%s' % self.field) if not self.dirs else '',
            '-' if (not self.dirs and self.field != 'title') else '',
            '%title' if self.field != 'title' else '')
        self.config.add({'link_format': default_link_format})
        self.link_format = self.config['link_format'].get()

    def flink(self, item):
        link_path = resolve_template(os.path.join(self.link_rel_dir,
                                     self.link_format), item)
        link_dir, link_name = os.path.split(link_path)
        last_dir = ''
        if self.dirs is True:
            last_dir = item[self.field]
        elif self.dirs == 'initial':
            last_dir = item[self.field][0]
        if self.buckets:
            bucket = find_bucket(link_dir, item[self.field])
            if not bucket:
                print("Found no folder defining a compatible "
                      "range for '%s'" % item[self.field])
            else:
                last_dir = os.path.join(bucket, last_dir)
        if last_dir:
            link_dir = os.path.join(link_dir, last_dir)

        create_dir(link_dir)
        dest = os.path.join(link_dir, link_name)
        if not os.path.exists(dest):
            print('Linking %s' % dest)
            os.symlink(item['filename'], dest)
