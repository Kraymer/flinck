#!/usr/bin/python
# -*- coding: utf-8 -*-

"""IMDB movie searcher.
"""

from __future__ import print_function

import os
import re
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

import omdb
import requests

from .config import config, FIELDS

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


def google_search_by(title, year):
    engine_id = '009217259823014548361:0gf2jfpzpbm'
    url = (u'https://www.googleapis.com/customsearch/v1?key='
        '%s&cx=%s&q=%s+%s' % (config['google_api_key'], engine_id,
            quote(title), year))
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()['items'][0]['link'].strip('/').split('/')[-1]


def format_field(item, field):
    """Tweak the string representation of the item field
    """
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
                item['decade'] = item['year'].strip(u'–')[:-1] + '0s'
            elif field == 'rating':
                item['rating'] = item.pop('imdb_rating')
        except Exception:
            item[field] = 'Unknown'


def format_item(item, fields):
    """Strip item from needless keys, format others values adequately
    """
    for key in item.keys():
        if key not in FIELDS:
            item.pop(key, None)
    for field in fields:
        format_field(item, field)
    return item


def search_by(title, year, fields, verbose, imdb_id=None):
    """Search movie infos using its title and year
    """
    if (title, year) in CACHED_RESULTS:
        item = CACHED_RESULTS[(title, year)]
        if verbose > 1:
            print('Get from cache: %s' % item)
    else:
        query = {'fullplot': False, 'tomatoes': False}
        if imdb_id:
            query['imdbid'] = imdb_id
        else:
            query['title'] = title
            query['year'] = year
        if verbose > 1:
            print('Query: %s' % query)
        item = omdb.get(**query)
        if item:
            item = format_item(item, fields)
            CACHED_RESULTS[(title, year)] = item
        else:
            imdb_id = google_search_by(title, year)
            if imdb_id:
                item = search_by(title, year, fields, verbose, imdb_id)
                item['title'] = title  # force original title
                return item
    return item

def search_filename(fname, fields, verbose):
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
