#!/usr/bin/python
# -*- coding: utf-8 -*-

"""IMDB movie searcher.
"""

from __future__ import print_function

import os
import re
from unidecode import unidecode
import omdb
from .config import FIELDS

# Regex to extract title and year. Should work as long as they are at the
# beginning and in that order.
FNAME_SPLIT_RE = '|'.join([r'\W%s(?:\W|$)' % x
                           for x in ('dvdrip', r'vost\w+', '1080p',
                                     '720p', 'multi',
                                     r'[\(\[]\D+[\)\]]',  # parentheses
                                     'bluray', 'x264', 'ac3',  # format
                                     r'b[dr]rip', 'xvid', 'divx', 'fansub',
                                     r'S\d+(E\d+)?',      # seasons
                                     'avi', 'mkv')])
CACHED_RESULTS = {}


def scrub(text, chars, new):
    """Replace chars.
    """
    for char in chars:
        if char in text:
            text = text.replace(char, new)
    return text.strip()


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


def search_by(title, year, fields, verbose=0):
    """Search movie infos using its title and year
    """
    if (title, year) in CACHED_RESULTS:
        item = CACHED_RESULTS[(title, year)]
        if verbose > 1:
            print('Get from cache: %s' % item)
    else:
        query = {'fullplot': False, 'tomatoes': False, 'title': title,
            'year': year}
        if verbose > 1:
            print('Query: %s' % query)
        item = omdb.get(**query)
        if item:
            for key in item.keys():
                if key not in FIELDS:
                    item.pop(key, None)
            for field in fields:
                format_field(item, field)
        CACHED_RESULTS[(title, year)] = item
    return item

def search_filename(fname, fields, verbose=0):
    """Extract movie title/date from filename and return dict with movies infos
    """
    path_tokens = os.path.normpath(fname).split(os.sep)
    candidate = path_tokens[-1]
    res = re.split(FNAME_SPLIT_RE, candidate,
                   flags=re.I | re.U)[0].strip()
    res = scrub(res, '[({])}', ' ')
    res = ' '.join([x for x in re.split(r'[\s\._]', res, flags=re.U) if x])
    years = re.findall(r'((?:19|20)\d\d)', res)
    if years:
        toks = re.split(r'(%s)' % years[-1], res)
    else:
        toks = [res]
    title = toks[0].strip() # unidecode(toks[0].strip())
    year = toks[1] if len(toks) > 1 else None
    item = search_by(title, year, fields, verbose)
    if item:
        item['filename'] = fname
        return item
