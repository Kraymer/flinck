#!/usr/bin/python
# -*- coding: utf-8 -*-

"""IMDB movie searcher.
"""

import os
import re
import sys

from imdb import IMDb

# Regex to extract title and year. Should work as long as they are at the
# beginning and in that order.
PATTERNS = [r'\W%s(?:\W|$)' % x for x in ('dvdrip', 'vost\w+', '1080p',
        '720p', 'multi',
         '[\(\[]\D+[\)\]]',  # parentheses
         'bluray', 'x264', 'ac3',  # format
         'b[dr]rip', 'xvid', 'divx', 'fansub',
         'S\d+(E\d+)?',  # seasons
         '(true)?french',  # langs
         'avi', 'mkv')]

imdb = IMDb()


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
    res = re.split(r'|'.join(PATTERNS), os.path.basename(fname),
                   flags=re.I | re.U)[0].strip()
    res = scrub(res, u'[({])}', u' ')
    res = u' '.join([x for x in re.split(r'[\s\._]', res, flags=re.U) if x])
    years = re.findall(r'((?:19|20)\d\d)', res)
    if years:
        toks = re.split(r'(%s)' % years[-1], res)
    else:
        toks = [res]
    title = toks[0]
    year = toks[1] if len(toks) > 1 else None
    title_year = title
    if year:
        title_year += '(%s)' % year
    try:
        items = imdb.search_movie(title_year)
    except imdb.IMDbError, e:
        print "Probably you're not connected to Internet. Error report: %s" % e
        sys.exit(3)
    if len(items) and (not year or (abs(items[0]['year'] - int(year))) <= 1):
        item = items[0]
        imdb.update(item)
        item_dict = {}
        for k in ('country', 'director', 'rating', 'runtime', 'year'):
            try:
                if not isinstance(item[k], basestring):
                    item_dict[k] = str(item[k])
                else:
                    item_dict[k] = item[k]
            except KeyError:
                item_dict[k] = 'Unknown'
        item_dict['title'] = title
        item_dict['genre'] = item['genre'][0]
        item_dict['filename'] = fname
        item_dict['decade'] = str(item_dict['year'])[:-1] + '0s'
        return item_dict
