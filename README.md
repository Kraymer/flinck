[![nopypi travis](https://travis-ci.org/Kraymer/flinck.svg?branch=master)](https://travis-ci.org/Kraymer/flinck)
[![nopypi pypi](http://img.shields.io/pypi/v/flinck.svg)](https://pypi.python.org/pypi/flinck)
[![nopypi downloads](https://pepy.tech/badge/flinck)](https://pepy.tech/project/flinck)
[![nopypi rtfd](https://readthedocs.org/projects/flinck/badge/?version=latest)](http://flinck.readthedocs.io/en/latest/?badge=latest)
[![nopypi rss](https://img.shields.io/badge/rss-subscribe-orange.svg)](https://github.com/Kraymer/flinck/releases.atom)

![nopypi logo](https://raw.githubusercontent.com/Kraymer/flinck/master/docs/_static/logo.png)

## flinck 

> /flingk/  
>     1. *verb tr.* to create a symlink to a movie (flick)  
>     2. *n.* CLI tool to organize your movies into a browsable directory tree 
>     offering fast access by dates, imdb ratings, etc

## Description

![](https://raw.githubusercontent.com/Kraymer/flinck/master/docs/_static/screenshot.png)

-   smart extraction of movie name from its folder/file, use
    [OMDB](http://www.omdbapi.com/) api to get infos
-   sane limited set of configuration options, yet highly flexible
    directories resulting structure
-   possible to split links into alphabetical buckets (A-C, D-F, etc)
    for large libraries

## Install

flinck is written for [Python 2.7](https://www.python.org/downloads/)
and [Python 3](https://www.python.org/downloads/).

Install with [pip](https://pip.pypa.io/en/stable/) via
`pip install flinck` command.

If you're on Windows and don't have pip yet, follow [this
guide](https://pip.pypa.io/en/latest/installing/) to install it.

## Usage

    Usage: flinck.py [OPTIONS] FILE|DIR

      Organize your movie collection using symbolic links.

    Options:
      -l, --link_dir PATH             Links root directory
      -b, --by [country|decade|director|genre|rating|runtime|title|year]
                                      Organize medias by...
      -v, --verbose
      --version                       Show the version and exit.
      -h, --help                      Show this message and exit.

      Example: flinck -l ./ --by genre --by rating ~/Movies

More infos on the [documentation website](http://flinck.readthedocs.io/)

## Example of configuration

`~/.config/flinck/config.yaml` corresponding to the screenshot above : :

    link_root_dir: '/Volumes/Disque dur/Movies'

    genre:
        dirs: true
        buckets: true

    rating:
        link_format: %rating-%year-%title
        dirs: false
        buckets: true

    decade:
        dirs: true

## Changelog

Available on [Github Releases
page](https://github.com/Kraymer/flinck/releases).

Want to know when new releases are shipped? Subscribe to the [Versions rss 
feed](http://createfeed.fivefilters.org/extract.php?url=https%3A%2F%2Fgithub.com%2FKraymer%2Fflinck%2Freleases&in_id_or_class=release-title&url_contains=).

## Feedbacks

Please submit bugs and features requests on the [Issue
tracker](https://github.com/Kraymer/flinck/issues).
