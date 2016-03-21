.. image:: https://raw.githubusercontent.com/Kraymer/flinck/master/docs/_static/logo.png
=====================

     [flingk]
      1. *verb tr., slang.* To create a symlink to a movie (flick)

Description
-----------

CLI tool to organize your movies into a browsable directory tree offering fast access by dates, imdb ratings, etc

.. image:: https://raw.githubusercontent.com/Kraymer/flinck/master/docs/_static/screenshot.png

Features
--------

- smart extraction of movie name from its folder/file, use IMDB api to get infos
- sane limited set of configuration options, yet highly flexible directories resulting structure
- possible to split links into alphabetical buckets (A-C, D-F, etc) for large libraries

Usage
-----

::

    usage: flinck.py [-h] [-l LINK_DIR] [-f] --by
                     {country,director,decade,genre,rating,runtime,title,year}
                     [{country,director,decade,genre,rating,runtime,title,year} ...]
                     FILE|DIR

    Organize your movie collection using symbolic links

    positional arguments:
      FILE|DIR              Media file or directory

    optional arguments:
      -h, --help            show this help message and exit
      -l LINK_DIR, --link_dir LINK_DIR
                            Links directory
      -f, --full-dir-scan   Link all files, not just the new ones
      --by {country,director,decade,genre,rating,runtime,title,year} [{country,director,decade,genre,rating,runtime,title,year} ...]
                            Organize medias by...

Configuration
-------------

