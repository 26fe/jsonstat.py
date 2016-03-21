===============
Jsonstat Module
===============

Contents:

.. toctree::
   :maxdepth: 2

   api_jsonstat_dimension

.. automodule:: jsonstat
    :members:

Utility functions
=================

.. autofunction:: jsonstat.from_file

.. autofunction:: jsonstat.from_json

.. autofunction:: jsonstat.from_string

.. autofunction:: jsonstat.cache_dir

.. autofunction:: jsonstat.from_url

.. autofunction:: jsonstat.download


Class hierarchy
===============

JsonStatCollection
==================

.. autoclass:: JsonStatCollection

    .. automethod:: JsonStatCollection.dataset
    .. special-members:: JsonStatCollection.__len__


JsonStatDataSet
===============

.. autoclass:: JsonStatDataSet
    :special-members: JsonStatDataSet.__len__

    .. automethod:: JsonStatDataSet.__init__
    .. automethod:: JsonStatDataSet.info
    .. automethod:: JsonStatDataSet.dimension
    .. automethod:: JsonStatDataSet.dimensions
    .. automethod:: JsonStatDataSet.value
    .. automethod:: JsonStatDataSet.status
    .. automethod:: JsonStatDataSet.to_table
    .. automethod:: JsonStatDataSet.to_data_frame


Downloader helper
=================

.. autoclass:: Downloader

    .. automethod:: Downloader.cache_dir
    .. automethod:: Downloader.download
