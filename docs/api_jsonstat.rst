===============
Jsonstat Module
===============

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

JsonStatDataSet
===============

.. autoclass:: JsonStatDataSet

    .. automethod:: JsonStatDataSet.__init__
    .. automethod:: JsonStatDataSet.__len__
    .. automethod:: JsonStatDataSet.info
    .. automethod:: JsonStatDataSet.dimension
    .. automethod:: JsonStatDataSet.dimensions
    .. automethod:: JsonStatDataSet.value
    .. automethod:: JsonStatDataSet.status
    .. automethod:: JsonStatDataSet.to_table
    .. automethod:: JsonStatDataSet.to_data_frame

JsonStatDimension
=================

.. autoclass:: JsonStatDimension

    .. automethod:: JsonStatDimension.info
    .. automethod:: JsonStatDimension.idx2pos

Downloader helper
=================

.. autoclass:: Downloader

    .. automethod:: Downloader.cache_dir
    .. automethod:: Downloader.download
