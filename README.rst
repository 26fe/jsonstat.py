===========
jsonstat.py
===========

.. image:: https://travis-ci.org/26fe/jsonstat.py.svg?branch=master
    :target: https://travis-ci.org/26fe/jsonstat.py

.. image:: https://readthedocs.org/projects/jsonstatpy/badge/?version=latest
    :target: http://jsonstatpy.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

Library for reading **JSON-stat** [1]_ format  data
The JSON-stat format is a JSON format for publishing dataset.
JSON-stat format is used by eurostat and Istat (Italian National Institute of Statistics)
and other institutions to publish statistical data.

***jsonstat.py*** contains an useful classes to explore istat api.

**jsonstat.py** library tries to mimic as much is possible the javascript library
and to be helpful in exploring dataset using ipython notebook.
For an example how to use it in junypter notebook see the example-notebook directory.

There is another python library **pyjstat** useful to read and write json-stat format.
The main focus of the previous library is to translate json-stat format into pandas dataframe.

WARNING: this is a preliminary work. I hope to improve this project
if the time permits. For every comment feel free to contact me.

.. [1] http://json-stat.org/ for JSON-stat information

Installation
============

    pip install jsonstat

Usage
=====

See examples directory for python script
See examples-notebook directory for ipython notebook example

License
=======

**jsonstat.py** is provided under the LGPL license.
See LICENSE file.
