#!/usr/bin/python
# -*- coding: utf-8 -*-

"""IMDB movie searcher.
"""

from __future__ import print_function

import os
import re

import omdb

# Regex to extract title and year. Should work as long as they are at the
# beginning and in that order.
FNAME_SPLIT_RE = r'|'.join(['\W%s(?:\W|$)' % x
    for x in ('dvdrip', 'vost\w+', '1080p',
        '720p', 'multi',
        '[\(\[]\D+[\)\]]',  # parentheses
        'bluray', 'x264', 'ac3',  # format
        'b[dr]rip', 'xvid', 'divx', 'fansub',
        'S\d+(E\d+)?',  # seasons
        '(true)?french',  # langs
        'avi', 'mkv')])
CACHED_RESULTS = {}


def scrub(s, chars, new):
    """Replace chars.
    """
    for c in chars:
        if c in s:
            s = s.replace(c, new)
    return s.strip()


def format_field(item, field):
    if item.get(field, None) == 'N/A':
        item[field] = 'Unknown'
    else:
        try:
            if field in ('country', 'genre'):
                item[field] = item[field].split(',')[0]
            elif field == 'director':
                item[field] = item[field].replace(', ', ' and ')
            elif field == 'runtime':
                item[field] = re.findall(r'\d+', item['runtime']
                                         )[0].zfill(3) + ' min'
            elif field == 'decade':
                item['decade'] = item['decade'].strip('-')[:-1] + '0s'
            elif field == 'rating':
                item['rating'] = item.pop('imdb_rating')
        except Exception:
            item[field] = 'Unknown'


def search_filename(fname, fields):
    """Retrieve movie infos from filename.
    """
    path_tokens = os.path.normpath(fname).split(os.sep)
    for candidate in (path_tokens[-1], path_tokens[-2]):
        res = re.split(FNAME_SPLIT_RE, candidate,
                       flags=re.I | re.U)[0].strip()
        res = scrub(res, '[({])}', ' ')
        res = ' '.join([x for x in re.split(r'[\s\._]', res, flags=re.U) if x])
        years = re.findall(r'((?:19|20)\d\d)', res)
        if years:
            toks = re.split(r'(%s)' % years[-1], res)
        else:
            toks = [res]
        title = toks[0].strip()
        year = toks[1] if len(toks) > 1 else None
        query = {'fullplot': False, 'tomatoes': False, 'title': title}
        if year:
            query['year'] = year
        if (title, year) in CACHED_RESULTS:
            item = CACHED_RESULTS[(title, year)]
        else:
            item = omdb.get(**query)
            if item:
                for f in fields:
                    format_field(item, f)
            CACHED_RESULTS[(title, year)] = item
        if item:
            item['filename'] = fname
            return item
