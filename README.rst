###########
jsonstat.py
###########

.. image:: https://travis-ci.org/26fe/jsonstat.py.svg?branch=master
    :target: https://travis-ci.org/26fe/jsonstat.py

.. image:: https://readthedocs.org/projects/jsonstatpy/badge/?version=latest
    :target: http://jsonstatpy.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://badge.fury.io/py/jsonstat.py.png
    :target: https://badge.fury.io/py/jsonstat.py

**jsonstat.py** is a library for reading the `**JSON-stat** <http://json-stat.org/>`_ data format
maintained and promoted by `Xavier Badosa <https://xavierbadosa.com/>`_.
The JSON-stat format is a JSON format for publishing dataset.
JSON-stat is used by several institutions to publish statistical data.
For example it is used by `Eurostat <http://ec.europa.eu/eurostat/>`_
that provide statistical information about the European Union (EU)
and `Istat <http://www.istat.it/en/>`_,
the  Italian National Institute of Statistics)

**jsonstat.py** library tries to mimic as much is possible in pythonn
the `json-stat Javascript Toolkit <https://json-stat.com/>`_
One of the objectives is to be helpful in exploring dataset
using ipython notebook.

For a fast overview of the feature you can start from this example notebook
`oecd-canada-jsonstat_v1.html <http://jsonstatpy.readthedocs.org/en/latest/notebooks/oecd-canada-jsonstat_v1.html>`_

You can also check out some of the jupyter example notebook from the
`example directory on github <https://github.com/26fe/jsonstat.py/tree/master/examples-notebooks>`_
or into the `documentation <http://jsonstatpy.readthedocs.org/en/latest>`_

As bonus **jsonstat.py** contains an useful classes to explore dataset
publiched by Istat.

You can find useful another python library
`pyjstat <https://pypi.python.org/pypi/pyjstat>`_
by Miguel Expósito Martín concerning json-stat format.
Its main focus is to translate json-stat format into pandas dataframe.

This library is in beta status.
I am actively working on it and hope to improve this project.
For every comment feel free to contact me gf@26fe.com

You can find source at `github <https://github.com/26fe/jsonstat.py>`_ ,
where you can open a `ticket <https://github.com/26fe/jsonstat.py/issues>`_, if you wish.

You can find the generated documentation at `readthedocs <http://jsonstatpy.readthedocs.org/en/latest/>`_.

************
Installation
************

Pip will install all required dependencies. For installation:

    pip install jsonstat

*****
Usage
*****

Simple Usage
************

There is a simple command line interface, so you can experiment to parse jsonstat file without write code::

    # parsing collection
    $ jsonstat --cache_dir /tmp http://json-stat.org/samples/oecd-canada.json
    downloaded file(s) are stored into '/tmp'
    download 'http://json-stat.org/samples/oecd-canada.json'
    JsonstatCollection contains the following JsonStatDataSet:
    0: dataset 'oecd'
    1: dataset 'canada'

    # parsing dataset
    $ jsonstat --cache_dir /tmp  "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/tesem120?sex=T&precision=1&age=TOTAL&s_adj=NSA"
    downloaded file(s) are stored into '/tmp'
    download 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/tesem120?sex=T&precision=1&age=TOTAL&s_adj=NSA'
    name:   'Unemployment rate'
    label:  'Unemployment rate'
    size: 461
    5 dimensions:
      0: dim id: 's_adj' label: 's_adj' size: '1' role: 'None'
      1: dim id: 'age' label: 'age' size: '1' role: 'None'
      2: dim id: 'sex' label: 'sex' size: '1' role: 'None'
      3: dim id: 'geo' label: 'geo' size: '39' role: 'None'
      4: dim id: 'time' label: 'time' size: '12' role: 'None'

code example::

    url = 'http://json-stat.org/samples/oecd-canada.json'
    collection = jsonstat.from_url(json_string)

    # print list of dataset contained into the collection
    collection.info()

    # select the first dataset of the collection and print a short description
    oecd = collection.dataset(0)
    oecd.info()

    # print description about each dimension of the dataset
    for d in oecd.dimensions():
        d.info()

    # print a datapoint contained into the dataset
    print(oecd.value(area='IT', year='2012'))

    # convert a dataset in pandas dataframe
    df = oecd.to_data_frame('year')

For more python script examples see
`examples directory <https://github.com/26fe/jsonstat.py/tree/master/examples>`_

For jupyter (ipython) notebooks see
`examples-notebooks directory <https://github.com/26fe/jsonstat.py/tree/master/examples-notebooks>`_

License
=======

**jsonstat.py** is provided under the LGPL license.
See LICENSE file.
