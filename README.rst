.. image:: https://raw.githubusercontent.com/Kraymer/flinck/master/docs/_static/logo.png

=====

     [flingk]
       *verb tr.* To create a symlink to a movie (flick)


Description
-----------

CLI tool to organize your movies into a browsable directory tree offering fast access by dates, imdb ratings, etc

.. image:: https://raw.githubusercontent.com/Kraymer/flinck/master/docs/_static/screenshot.png

Features
--------

- smart extraction of movie name from its folder/file, use IMDB api to get infos
- sane limited set of configuration options, yet highly flexible directories resulting structure
- possible to split links into alphabetical buckets (A-C, D-F, etc) for large libraries

Install
-------

flinck is written for `Python 2.7`_ and `Python 3`_.

Install with `pip`_ via ``pip install flinck`` command.

If you're on Windows and don't have pip yet, follow
`this guide`_ to install it.

.. _Python 2.7: https://www.python.org/downloads/
.. _Python 3: https://www.python.org/downloads/
.. _pip: https://pip.pypa.io/en/stable/
.. _this guide: https://pip.pypa.io/en/latest/installing/

Usage
-----

::

    usage: flinck.py [-h] [-l LINK_DIR] --by
                     {country,director,decade,genre,rating,runtime,title,year}
                     [{country,director,decade,genre,rating,runtime,title,year} ...]
                     FILE|DIR

    Organize your movie collection using symbolic links

    Example: flinck ~/Movies --by genre rating

More infos on `Wiki`_

.. _Wiki: https://github.com/Kraymer/flinck/wiki

Configuration
-------------

``~/.config/flinck/config.yaml`` corresponding to the screenshot above : ::

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

Top settings:

- **link_root_dir**: where the folders tree will be created. Must exist beforehand.
- **file_extensions**: files types to consider. Default: ``['avi', 'm4v', 'mkv', 'mp4']``
- **file_min_size_mb**: files whose size is below that threshold are ignored. Default: ``20``
- **google_api_key**: your `Google API key`_ (to enable the Google Custom Search backend)

Then, you can define a section for each metadata field you want to sort by.
Inside it, available settings are :

- **root**: root dirname (or relative path from ``link_root_dir``) for this metadata field. Default: the metadata field name.
- **link_format**: symlink naming format. Default: ``%title-%field``
- **dirs**: put symlinks into an intermediary directory named after the field value. Default: ``no``
- **buckets**: put symlinks into a parent matching directory if it does exist. Any directory that contains the field value or defines a matching range is valid.
  A range is defined by ``[]`` chars, eg *[A-D]* directory matches *Drama* genre field value.

.. _Google API key: https://code.google.com/apis/console

