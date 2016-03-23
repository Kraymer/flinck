.. image:: https://raw.githubusercontent.com/Kraymer/flinck/master/docs/_static/logo.png
=====================

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

Usage
-----

::

    usage: flinck.py [-h] [-l LINK_DIR] [-f] --by
                     {country,director,decade,genre,rating,runtime,title,year}
                     [{country,director,decade,genre,rating,runtime,title,year} ...]
                     FILE|DIR

    Organize your movie collection using symbolic links


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

Then, you can define a section for each metadata field you want to sort by.  
Inside it, available settings are :

- **root**: root dirname (or relative path from ``link_root_dir``) for this metadata field. Default: the metadata field name.
- **link_format**: symlink naming format. Default: ``%title-%field``
- **dirs**: put symlinks into an intermediary directory named after the field value. Default: ``no``
- **buckets**: put symlinks into a parent matching directory if it does exist. Any directory that contains the field value or defines a matching range is valid.  
  A range is defined by ``[]`` chars, eg *[A-D]* directory matches *Drama* genre field value.



