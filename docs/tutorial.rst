Tutorial
========

.. testsetup:: *

   import jsonstat

The parrot module is a module about parrots.

Doctest example:

.. doctest::

   >>> 2 + 2
   4

Test-Output example:

.. testcode::

    json_string = '''
    {
        "label" : "concepts",
        "category" : {
            "index" : {
                "POP" : 0,
                "PERCENT" : 1
            },
            "label" : {
                "POP" : "population",
                "PERCENT" : "weight of age group in the population"
            },
            "unit" : {
                "POP" : {
                    "label": "thousands of persons",
                    "decimals": 1,
                    "type" : "count",
                    "base" : "people",
                    "multiplier" : 3
                },
                "PERCENT" : {
                    "label" : "%",
                    "decimals": 1,
                    "type" : "ratio",
                    "base" : "per cent",
                    "multiplier" : 0
                }
            }
        }
    }
    '''
    print(2 + 2)

This would output:

.. testoutput::

   4




.. testcode::

   >>> json_string_dimension_sex = '''
    ... {
    ...     "label" : "sex",
    ...     "category" : {
    ...       "index" : {
    ...         "M" : 0,
    ...         "F" : 1,
    ...         "T" : 2
    ...       },
    ...       "label" : {
    ...         "M" : "men",
    ...         "F" : "women",
    ...         "T" : "total"
    ...       }
    ...     }
    ... }
    ... '''
    >>> dim = JsonStatDimension(did="sex").from_string(json_string_dimension_sex)
    >>> len(dim)
    3

This would output:

.. testoutput::

   4



