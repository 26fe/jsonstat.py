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

 collection := {
                 [ "version" ":" `string` ]
                 [ "class" ":" "collection" ]
                 [ "href" ":" `url` ]
                 [ "updated": `date` ]
                 link : {
                     item : [
                         ( dataset )+
                     ]
              }
 dataset := {
        "version"   : <version>
        "class"     : "dataset",
        "href"      : <url>
        "label"     : <string>
        "id"        : [ <string>+]           # ex. "id" : ["metric", "time", "geo", "sex"],
        "size"      : [ <int>, <int>, ... ]
        "role"      : roles of dimension
        "value"     : [<int>, <int> ]
        "status"    : status
        "dimension" : { <dimension_id> : dimension, ...}
        "link"      :
        }

 dimension_id := <string>

 # possible values of dimension are called categories
 dimension := {
        "label" : <string>
        "class" : "dimension"
        "category: {
                  "index"       : dimension_index
                  "label"       : dimension_label
                  "child"       : dimension_child
                  "coordinates" :
                  "unit"        : dimension_unit
                   }
        }

 dimension_index :=
                    { <cat1>:int, ....}      # { "2003" : 0, "2004" : 1, "2005" : 2, "2006" : 3 }
                 |
                    [ <cat1>, <cat2> ]   # [  2003, 2004 ]

dimension_label  :=
                    { lbl1:idx1



