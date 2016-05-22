#!/usr/bin/python
# -*- coding: utf-8 -*-

"""IMDB movie searcher.
"""

from __future__ import print_function

import logging
import os
import re
import sys
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
logger = logging.getLogger(__name__)


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
        json = r.json()
        if 'items' in json:
            return r.json()['items'][0]['link'].strip('/').split('/')[-1]


def format_item(item):
    """Tweak the string representation of the item field
    """
    for field in set(list(item) + list(FIELDS)):
        if item.get(field, None) == 'N/A':
            item[field] = 'Unknown'
    try:
        for field in ('country', 'genre'):
            item[field] = item[field].split(',')[0]
        item['director'] = item['director'].replace(', ', ' and ')
        item['runtime'] = re.findall(r'\d+', item['runtime']
                                     )[0].zfill(3) + ' min'
        item['decade'] = item['year'].strip(u'–')[:-1] + '0s'
        item['rating'] = item.pop('imdb_rating')
    except Exception:
        item[field] = 'Unknown'
    return item


def to_unicode(text):
    try:
        return unicode(text, sys.getfilesystemencoding(), errors="ignore")
    except NameError:
        pass  # Python3, no conversion needed
    return text


def search_by(title, year, fields, imdb_id=None):
    """Search movie infos using its title and year
    """
    if (title, year) in CACHED_RESULTS:
        item = CACHED_RESULTS[(title, year)]
        logger.debug('Get from cache: %s' % item)
    else:
        query = {'fullplot': False, 'tomatoes': False}
        if imdb_id:
            query['imdbid'] = imdb_id
        else:
            query['title'] = title
            query['year'] = year
        logger.debug('Query: %s' % query)
        item = omdb.get(**query)
        if item:
            item['title'] = to_unicode(title)  # force original title
            item = format_item(item)
            CACHED_RESULTS[(title, year)] = item
        elif not imdb_id and config['google_api_key']:
            imdb_id = google_search_by(title, year)
            if imdb_id:
                item = search_by(title, year, fields, imdb_id)
    return item

def search_filename(fname, fields):
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
    title = toks[0].strip()
    year = toks[1] if len(toks) > 1 else None
    item = search_by(title, year, fields)
    if item:
        item['filename'] = fname
        return item
