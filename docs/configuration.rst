Configuration
=============

To configure flinck, you create a file called ``config.yaml``. The location of the file depend on your platform:

- on Unix-like OSes, write ``~/.config/flinck/config.yaml``
- on Windows, use ``%APPDATA%\flinck\config.yaml``. This is usually in a directory like C:\Users\You\AppData\Roaming.
- on OS X, you can use either the Unix location or ``~/Library/Application Support/flinck/config.yaml``

The config file uses YAML syntax, most configuration options are simple key/value pairs.


Global options
--------------

link_root_dir
^^^^^^^^^^^^^

Where the folders tree containing the symlinks will be created.
This directory must exist beforehand.

file_extensions
^^^^^^^^^^^^^^^

Files extensions of movies to symlink.

Default: ``['avi', 'm4v', 'mkv', 'mp4']``

file_min_size_mb
^^^^^^^^^^^^^^^^

Files smaller than that threshold are ignored.

Default: ``20``

google_api_key
^^^^^^^^^^^^^^

A key of 39 alphanumeric characters long to enable the Google Custom Search
backend. Registering one is free and can be done on `Google API console`_
page.

**Why use it?**

Because flinck extract movie titles from filenames to perform its `OMDb`_
queries, having movie name into filename is required. More than that, storing
US movie name is required as OMDb won't give result for a query using the
original movie name.

If you prefer to name your files using the original title, entering a
`google_api_key` is thus required to have good results when symlinking.

.. _Google API console: https://code.google.com/apis/console
.. _OMDb: http://www.omdbapi.com/

Attributes options
------------------

You can define a section for each metadata field you want to sort by.

root
^^^^

Root dirname (or relative path from `link_root_dir`) for this metadata field.

Default: the metadata field name.

link_format
^^^^^^^^^^^

Naming format used for symlinks.
You can use any attribute prefixed by ``%``, ``%field`` being a shortcut that
designates the attribute of the current section.

Default: ``%title-%field``

dirs
^^^^

Put symlinks into an intermediary directory named after the field value?

Default: ``no``

buckets
^^^^^^^

Put symlinks into a parent matching directory if it does exist.

Default: ``no``

Any directory defining a matching range (see :ref:`bucket-matching`) is valid  ; eg if you create a *[A-D]*
directory and activates ``buckets`` in your *genre* section then movies having
*Drama* as genre will be symlinked into it.

.. _bucket-matching:

Bucket matching
"""""""""""""""

Here are the three possibles syntaxes to use when defining buckets directory.
Say you want to split movies into three groups : those having imdb ratings respectively lower/equal/higher than 7.x

- **lower bound match** : use the ``+`` suffix to indicate a lower bound.
  eg *'1+'* directory captures all existing ratings
- **substring match** : if tested value starts with directory name, the latter is selected.
  eg *'7'* directory capture all 7.x ratings
- **range match** : use the ``[-]`` to indicate a range.
  eg *'[8-9]'* captures the 8.x and 9.x ratings

When multiple directories match, the one which matches more closely is selected.

