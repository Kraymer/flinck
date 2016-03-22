.. image:: https://raw.githubusercontent.com/Kraymer/flinck/master/docs/_static/logo.png
=====================

     [flingk]
      1. *verb tr., slang.* To f*ckin create a symlink to a movie (flick)

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

`~/.config/flinck/config.yaml` corresponding to the screenshot above : ::

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
        
- ``link_root_dir`` : where the folders tree will be created. Must exist beforehand.

Then, you can define a section for each metadata you want to sort by.
Available settings are :

- ``as`` : dirname (or relative path from ``link_root_dir``) where to grow the three
- ``link_format`` : symlink format template
- ``dirs``: create [TO BE CONTINUED]



