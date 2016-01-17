=======
jsonstat.py
=======

.. image:: https://travis-ci.org/26fe/jsonstat.py.svg?branch=master
    :target: https://travis-ci.org/26fe/jsonstat.py


**jsonstat** is a python library for reading **JSON-stat** [1]_ format  data
The JSON-stat format is a simple JSON format for data dissemination. 
JSON-stat format is used by eurostat and istat and other istitutions
to publish statistical data.

jsonstat contains an api useful to explore istat data set. 

There is another python library **pyjstat** useful to read and write json-stat format. 
The main focus of the previous library is to translate
json-stat format into pandas dataframe.

**jsonstat** library tries to mimic as much is possible the javascript library
and to be helpful in exploring dataset using ipython notebook See examples-notebook
For an example how to use it see the ipython notebook.

WARNING: this is a preliminary work. I hope to improve this project
if the time permits. For every comment feel free to contact me.

For now the library work only in python 2.7, but I am working on running on python 3.5


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

**jsonstat** is provided under the LGPL license.
See LICENSE file.

