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


def scrub(s, chars, new):
    """Replace chars.
    """
    for c in chars:
        if c in s:
            s = s.replace(c, new)
    return s.strip()


def search_filename(fname):
    """Retrieve movie infos from filename.
    """
    if os.path.basename(fname).lower().startswith('sample'):
        return
    res = re.split(FNAME_SPLIT_RE, os.path.basename(fname),
                   flags=re.I | re.U)[0].strip()
    res = scrub(res, '[({])}', ' ')
    res = ' '.join([x for x in re.split(r'[\s\._]', res, flags=re.U) if x])
    years = re.findall(r'((?:19|20)\d\d)', res)
    if years:
        toks = re.split(r'(%s)' % years[-1], res)
    else:
        toks = [res]
    year = toks[1] if len(toks) > 1 else None
    query = {'fullplot': False, 'tomatoes': False, 'title': toks[0]}
    if year:
        query['year'] = year
    print("Query: %s" % query)
    item = omdb.get(**query)
    if item:
        for k in item:
            if item[k] == 'N/A':
                item[k] = 'Unknown'
        item['country'] = item['country'].split(',')[0]
        item['director'] = item['director'].replace(', ', ' and ')
        item['genre'] = item['genre'].split(',')[0]
        item['runtime'] = re.findall(r'\d+', item['runtime']
                                     )[0].zfill(3) + ' min'
        item['filename'] = fname
        item['decade'] = item['year'].strip('-')[:-1] + '0s'
        item['rating'] = item.pop('imdb_rating')
        return item
    # exit(1)
