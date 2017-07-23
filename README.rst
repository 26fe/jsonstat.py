jsonstat.py
===========

.. image:: https://travis-ci.org/26fe/jsonstat.py.svg?branch=master
    :target: https://travis-ci.org/26fe/jsonstat.py

.. image:: https://readthedocs.org/projects/jsonstatpy/badge/?version=latest
    :target: http://jsonstatpy.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://badge.fury.io/py/jsonstat.py.png
    :target: https://badge.fury.io/py/jsonstat.py

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
   :target: https://saythanks.io/to/26fe

**jsonstat.py** is a library for reading the `JSON-stat <http://json-stat.org/>`_ data format
maintained and promoted by `Xavier Badosa <https://xavierbadosa.com/>`_.
The JSON-stat format is a JSON format for publishing dataset.
JSON-stat is used by several institutions to publish statistical data.
An incomplete list is:

- `Eurostat <http://ec.europa.eu/eurostat/>`_ that provide statistical information about the European Union (EU)

- `Italian National Institute of Statistics Istat <http://www.istat.it/en/>`_

- `Central Statistics Office of Ireland <cso.ie>`_

- `United Nations Economic Commission for Europe (UNECE) <http://www.unece.org/>`_
  statistical data are `here <http://w3.unece.org/pxweb/en/>`_

- `Statistics Norway <http://www.ssb.no/en>`_

- `UK Office for national statistics <https://www.ons.gov.uk/>`_
  see `here <https://blog.ons.digital/2014/08/04/introducing-the-new-improved-ons-api/>`_

- others...

**jsonstat.py** library tries to mimic as much is possible in python
the `json-stat Javascript Toolkit <https://json-stat.com/>`_.
One of the library objectives is to be helpful in exploring dataset
using jupyter (ipython) notebooks.

For a fast overview of the feature you can start from this example notebook
`oecd-canada-jsonstat_v1.html <http://jsonstatpy.readthedocs.org/en/latest/notebooks/oecd-canada-jsonstat_v1.html>`_
You can also check out some of the jupyter example notebook from the
`example directory on github <https://github.com/26fe/jsonstat.py/tree/master/examples-notebooks>`_
or from the `documentation <http://jsonstatpy.readthedocs.org/en/latest>`_

As bonus **jsonstat.py** contains an useful classes to explore dataset
published by `Istat <http://www.istat.it/en/>`_.

You can find useful another python library
`pyjstat <https://pypi.python.org/pypi/pyjstat>`_
by Miguel Expósito Martín concerning json-stat format.

This library is in beta status.
I am actively working on it and hope to improve this project.
For every comment feel free to contact me gf@26fe.com

You can find source at `github <https://github.com/26fe/jsonstat.py>`_ ,
where you can open a `ticket <https://github.com/26fe/jsonstat.py/issues>`_, if you wish.

You can find the generated documentation at `readthedocs <http://jsonstatpy.readthedocs.org/en/latest/>`_.

Installation
------------

Pip will install all required dependencies. For installation:

    pip install jsonstat.py

Usage
-----

Simple Usage
~~~~~~~~~~~~

There is a simple command line interface, so you can experiment to parse jsonstat file without write code::

    # parsing collection
    $ jsonstat info --cache_dir /tmp http://json-stat.org/samples/oecd-canada.json
    downloaded file(s) are stored into '/tmp'
    download 'http://json-stat.org/samples/oecd-canada.json'
    Jsonsta    tCollection contains the following JsonStatDataSet:
    +-----+----------+
    | pos | dataset  |
    +-----+----------+
    | 0   | 'oecd'   |
    | 1   | 'canada' |
    +-----+----------+

    # parsing dataset
    $ jsonstat info --cache_dir /tmp  "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/tesem120?sex=T&precision=1&age=TOTAL&s_adj=NSA"
    downloaded file(s) are stored into '/tmp'
    download 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/tesem120?sex=T&precision=1&age=TOTAL&s_adj=NSA'
    name:   'Unemployment rate'
    label:  'Unemployment rate'
    size: 467
    +-----+-------+-------+------+------+
    | pos | id    | label | size | role |
    +-----+-------+-------+------+------+
    | 0   | s_adj | s_adj | 1    |      |
    | 1   | age   | age   | 1    |      |
    | 2   | sex   | sex   | 1    |      |
    | 3   | geo   | geo   | 39   |      |
    | 4   | time  | time  | 12   |      |
    +-----+-------+-------+------+------+

code example::

    url = 'http://json-stat.org/samples/oecd-canada.json'
    collection = jsonstat.from_url(url)

    # print list of dataset contained into the collection
    print(collection)

    # select the first dataset of the collection and print a short description
    oecd = collection.dataset(0)
    print(oecd)

    # print description about each dimension of the dataset
    for d in oecd.dimensions():
        print(d)

    # print a datapoint contained into the dataset
    print(oecd.value(area='IT', year='2012'))

    # convert a dataset in pandas dataframe
    df = oecd.to_data_frame('year')

For more python script examples see
`examples directory <https://github.com/26fe/jsonstat.py/tree/master/examples>`_.

For jupyter (ipython) notebooks see
`examples-notebooks directory <https://github.com/26fe/jsonstat.py/tree/master/examples-notebooks>`_.

Support
-------

This is an open source project, maintained in my spare time.
Maybe a particular features or functions that you would like are missing.
But things don’t have to stay that way: you can contribute the project development yourself.
Or notify me and ask to implement it.

Bug reports and feature requests should be submitted
using the `github issue tracker <https://github.com/26fe/jsonstat.py/issues>`_.
Please provide a full traceback of any error you see and if possible a sample file.
If you are unable to make a file publicly available then contact me at gf@26fe.com.

You can find support also on the `google group <https://groups.google.com/forum/#!forum/json-stat>`_.

How to Contribute Code
----------------------

Any help will be greatly appreciated, just follow those steps:

1) Fork it. Start a new fork for each independent feature, don’t try to fix all problems at the same time,
   it’s easier for those who will review and merge your changes.

2) Create your feature branch (``git checkout -b my-new-feature``)

3) Write your code. Add unit tests for your changes!
   If you added a whole new feature, or just improved something, you can be proud of it,
   so add yourself to the ``AUTHORS`` file :-)
   Update the docs!
4) Commit your changes (``git commit -am 'Added some feature'``)

5) Push to the branch (``git push origin my-new-feature``)

6) Create new Pull Request. Click on the large "pull request" button on your repository.
   Wait for your code to be reviewed, and, if you followed all theses steps, merged into the main repository.

License
-------

**jsonstat.py** is provided under the LGPL license.
See LICENSE file.
