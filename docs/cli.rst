CLI usage
=========

::

    flinck.py [OPTIONS] FILE|DIR


flinck creates symlinks for each combination of movie
``FILE``/``--by ATTR`` it is given as input.

Optional flags:

- ``-l, --link_dir``: target root directory where symlinks are created.
  Required if not present in ``config.yaml``
- ``-b, --by``: which attribute(s) to consider. Specify multiple ones by
  repeating the ``-b ATTR`` flags as needed. Uses ``config.yaml`` sections as default attributes list.
- ``-v, --verbose``: log more details. Use twice for even more.
