===============
Jsonstat Module
===============

jsonstat module contains classes
and utility functions to parse `jsonstat data format <https://json-stat.org/>`_.


.. automodule:: jsonstat
    :members:

.. toctree::
   :maxdepth: 2

   api_jsonstat_utility
   api_jsonstat_collection
   api_jsonstat_dataset
   api_jsonstat_dimension
   api_jsonstat_downloader



::

 collection : {
                 [ "version" ":" `string` ]
                 [ "class" ":" "collection" ]
                 [ "href" ":" `url` ]
                 [ "updated": `date` ]
                 link : {
                     item : [
                         ( dataset )+
                     ]
              }
 item_list
