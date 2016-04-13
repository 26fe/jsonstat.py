JsonStatDataSet
===============

.. automodule:: jsonstat

.. autoclass:: JsonStatDataSet

    .. automethod:: JsonStatDataSet.__init__
    .. automethod:: JsonStatDataSet.name
    .. automethod:: JsonStatDataSet.label
    .. automethod:: JsonStatDataSet.__len__

dimensions
^^^^^^^^^^

    .. automethod:: JsonStatDataSet.dimension
    .. automethod:: JsonStatDataSet.dimensions
    .. automethod:: JsonStatDataSet.info_dimensions

querying methods
^^^^^^^^^^^^^^^^

    .. automethod:: JsonStatDataSet.data
    .. automethod:: JsonStatDataSet.value
    .. automethod:: JsonStatDataSet.status

transforming
^^^^^^^^^^^^

    .. automethod:: JsonStatDataSet.to_table
    .. automethod:: JsonStatDataSet.to_data_frame

parsing
^^^^^^^

    .. automethod:: JsonStatDataSet.from_file
    .. automethod:: JsonStatDataSet.from_string
    .. automethod:: JsonStatDataSet.from_json
