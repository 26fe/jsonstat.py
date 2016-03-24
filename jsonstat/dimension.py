# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file


"""
Documentazione!!!
"""


# stdlib
from __future__ import print_function
from __future__ import unicode_literals
from collections import namedtuple
import json

# packages
import terminaltables

# jsonstat
from jsonstat.exceptions import JsonStatException
from jsonstat.exceptions import JsonStatMalformedJson

JsonStatCategory = namedtuple('JsonStatCategory', ['label', 'index', 'pos'])


class JsonStatDimension:
    """Represents a JsonStat Dimension. It is contained into a JsonStat Dataset.

    example::

        "dimension" : {
            "concept" : {
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
            },
            "dim": {
            ...
            },
        }

    >>> json_string = '''{
    ...                    "label" : "concepts",
    ...                    "category" : {
    ...                       "index" : { "POP" : 0, "PERCENT" : 1 },
    ...                       "label" : { "POP" : "population",
    ...                                   "PERCENT" : "weight of age group in the population" }
    ...                    }
    ...                  }
    ... '''
    >>> dim = JsonStatDimension(name="concept", role="metric").from_string(json_string)
    >>> len(dim)
    2
    >>> dim.category(0).index
    'POP'
    >>> dim.category('POP').label
    'population'
    >>> dim.category(1)
    JsonStatCategory(label='weight of age group in the population', index='PERCENT', pos=1)
    >>> dim.info()
    +-----+-----------+-----------------------------------------+
    | pos | idx       | label                                   |
    +-----+-----------+-----------------------------------------+
    | 0   | 'POP'     | 'population'                            |
    | 1   | 'PERCENT' | 'weight of age group in the population' |
    +-----+-----------+-----------------------------------------+
    """

    def __init__(self, name=None, size=None, pos=None, role=None):
        """initialize a dimension

        :param name: name of dimension
        :param size: size of dimension (nr of values)
        :param pos: position of dimension into the dataset
        :param role: of dimension
        """

        # it is valid is correctly built (f.e. it was parsed correctly)
        self.__valid = False

        self.__name = name
        self.__size = size
        self.__role = role
        self.__pos = pos
        self.__label = None

        # if indexes are not present in json __idx2cat will be None
        # if labels  are not present in json __lbl2cat will be None
        self.__pos2cat = None
        self.__idx2cat = None
        self.__lbl2cat = None

    #
    # queries
    #   dimension properties

    def name(self):
        """name of dimension"""
        return self.__name

    def label(self):
        """label of this dimension"""
        return self.__label

    def role(self):
        """role of this dimension (time, geo or metric)"""
        return self.__role

    def pos(self):
        """position of this dimension respect to the dataset which dimension belongs to"""
        return self.__pos

    def __len__(self):
        """size of this dimension"""
        return self.__size

    def __str__(self):
        if self.__pos2cat is None:
            return ""

        lst = [["pos", "idx", "label"]]
        for cat in self.__pos2cat:
            idx = cat.index
            lbl = cat.label
            if idx is None: idx = ""
            if lbl is None: lbl = ""
            row = [str(cat.pos), "'" + idx + "'", "'" + lbl + "'"]
            row = list(map(lambda x: "" if x is None else x, row))
            lst.append(row)

        table = terminaltables.AsciiTable(lst)
        out = table.table

        # out = "index\n"
        # f = "{:>5} {:<8} {:<8}\n"
        # out += f.format('pos', 'idx', 'label')
        # for cat in self.__pos2cat:
        #     idx = cat.index
        #     lbl = cat.label
        #     if idx is None: idx = ""
        #     if lbl is None: lbl = ""
        #
        #     out += f.format(cat.pos, "'" + idx + "'", "'" + lbl + "'")
        return out

    def __repr__(self):
        """used by ipython to make a better representation"""
        return self.__str__()

    def info(self):
        """print some info on standard output about this dimension"""
        print(self)

    #
    # queries
    #   categories
    #

    def category(self, spec):
        if not self.__valid:
            raise JsonStatException("dimension {} is not initialized".format(self.__name))

        if isinstance(spec, int):
            cat = self.__pos2cat[spec]
            return cat

        # try first indexes
        if spec in self.__idx2cat:
            cat = self.__idx2cat[spec]
        elif spec in self.__lbl2cat:
            cat = self.__lbl2cat[spec]
        else:
            raise JsonStatException("dimension '{}': do not have index or label '{}'".format(self.__name, spec))

        return cat

    def _pos2cat(self, pos):
        """get the category associated with the position (integer)

        :param pos: integer
        :returns: the label or None if the label not exists at position pos
            JsonStatCategory(index='2013', label='2013', pos=pos)
        """
        if self.__pos2cat is None:
            return None
        else:
            return self.__pos2cat[pos]

    def _2pos(self, spec):
        """from spec to position

        :param spec: index or label or integer
        :returns: integer
        """
        if not self.__valid:
            raise JsonStatException("dimension {} is not initialized".format(self.__name))
        if spec in self.__idx2cat:
            return self.__idx2cat[spec].pos
        if self.__lbl2cat is not None and spec in self.__lbl2cat:
            return self.__lbl2cat[spec].pos
        if isinstance(spec, int) and spec < len(self.__pos2cat):
            return spec
        raise JsonStatException("dimension '{}': do not have index or label '{}'".format(self.__name, spec))

    def _idx2pos(self, idx):
        """from index to position

        :param idx: index for ex.: "2013"
        :returns: integer
        """
        if not self.__valid:
            raise JsonStatException("dimension '{}': is not initialized".format(self.__name))
        if idx not in self.__idx2cat:
            raise JsonStatException("dimension '{}': do not have index '{}'".format(self.__name, idx))
        return self.__idx2cat[idx].pos

    def _lbl2pos(self, lbl):
        """from label to position

        :param lbl: index for ex.: "2013"
        :returns: integer
        """
        if not self.__valid:
            raise JsonStatException("dimension '{}': is not initialized".format(self.__name))
        if lbl not in self.__idx2cat:
            raise JsonStatException("dimension '{}': do not have label {}".format(self.__name, lbl))
        return self.__lbl2cat[lbl].pos

    #
    # parsing methods
    #

    def from_string(self, json_string):
        """Parse a json string

        :param json_string:
        :returns: itself to chain call
        """
        json_data = json.loads(json_string)
        self.from_json(json_data)
        return self

    def from_json(self, json_data):
        """Parse a json structure representing a dimension id

        From `json-stat.org <https://json-stat.org/format/#dimensionid>`_

            It is used to describe a particular dimension.
            The name of this object must be one of the strings in the id array.
            There must be one and only one dimension ID object for every dimension in the id array.

        example::

            "dimension" : {
                "metric" : { … },
                "time" : { … },
                "geo" : { … },
                "sex" : { … },
                …
            }

        Parent: 'dimension'
        Children:
        - category
        - label
        - class

        :param json_data:
        :returns: itself to chain call
        """
        # children category, label, class
        if 'label' in json_data:
            self.__label = json_data['label']

        if 'class' in json_data:
            if json_data['class'] != 'dimension':
                msg = "class must be equals to 'dimension'"
                raise JsonStatMalformedJson(msg)

        # parsing category
        if "category" not in json_data:
            msg = "dimension '{}': missing category key".format(self.__name)
            raise JsonStatMalformedJson(msg)

        self.__parse_category(json_data['category'])

        self.__valid = True
        return self

    def __parse_category(self, json_data_category):
        """It is used to describe the possible values of a dimension.

        https://json-stat.org/format/#category
        category is required
        children of category:
          - index
          - label
          - child
          - coordinates
          - unit
        :param json_data_category:
        :returns:
        """

        # validate: label or index must be present
        if 'index' not in json_data_category and 'label' not in json_data_category:
            msg = "dimension '{}': one of keys 'label' or 'index' must be presents"
            raise JsonStatMalformedJson(msg)

        if 'index' in json_data_category:
            self.__parse_json_index(json_data_category)
        if 'label' in json_data_category:
            self.__parse_json_label(json_data_category)

        # validate: number of indexes and labels must the same??
        if self.__idx2cat is not None and self.__lbl2cat is not None:
            if len(self.__idx2cat) != len(self.__lbl2cat):
                # TODO: warning see hierarchy.json
                msg = "dimension '{}': the number of indexes ({}) are different of the numbers of labels ({})"
                msg = msg.format(self.__name, len(self.__idx2cat), len(self.__lbl2cat))
                # raise JsonStatMalformedJson(msg)
            if len(self.__idx2cat) < len(self.__lbl2cat):
                msg = "dimension '{}': the number of labels ({}) are greater than number of indexes ({})"
                msg = msg.format(self.__name, len(self.__lbl2cat), len(self.__idx2cat))
                raise JsonStatMalformedJson(msg)

        # validate: indexes must be consistent with size
        if self.__size != len(self.__idx2cat):
            msg = "dimension '{}': malformed json: number of indexes {} not match with size {}"
            msg = msg.format(self.__name, len(self.__idx2cat), self.__size)
            raise JsonStatMalformedJson(msg)

        # validate: no hole in the indexes
        if any(v is None for v in self.__pos2cat):
            msg = 'hole in index'
            raise JsonStatMalformedJson(msg)

        # TODO: parse 'unit'
        # "unit" : {
        # 	 "exp" : {
        # 			"decimals": 1,
        # 			"label" : "millions",
        # 			"symbol" : "$",
        # 			"position" : "start"
        # 	 }
        # }
        # 	"category" : {
        # 		"label" : {
        # 			"UNR" : "unemployment rate"
        # 		},
        # 		"unit" : {
        # 			"UNR" : {
        # 				"label" : "%",
        # 				"decimals" : 9,
        # 				"type" : "ratio",
        # 				"base" : "per cent",
        # 				"multiplier" : 0
        # 			}
        # 		}
        # 	}
        if 'unit' in json_data_category:
            if self.__role != "metric":
                msg = "dimension {}: 'unit' are used but dimension role must be 'metric'"
                JsonStatException(msg)
            self.__unit = json_data_category['unit']

    def __parse_json_index(self, json_data):
        """parse index json structure

        for ex. the json structure could be
        "category" : { "index" : { "2003" : 0, "2004" : 1, "2005" : 2, "2006" : 3 }
        :param json_data: json structure
        """

        if self.__size is None:
            self.__size = len(json_data['index'])

        self.__idx2cat = {}

        # preallocate a list of length self.size with default value None
        self.__pos2cat = self.__size * [None]

        if type(json_data['index']) is list:
            for pos, idx in enumerate(json_data['index']):
                self.__parse_json_index_helper(idx, pos)
        else:
            for idx, pos in json_data['index'].items():
                self.__parse_json_index_helper(idx, pos)

    def __parse_json_index_helper(self, idx, pos):
        if pos >= self.__size:
            msg = "index {} for dimension '{}' is greater than size {}".format(pos, self.__name, self.__size)
            raise JsonStatException(msg)

        cat = JsonStatCategory(pos=pos, index=idx, label=None)
        self.__pos2cat[pos] = cat
        self.__idx2cat[idx] = cat

    def __parse_json_label(self, json_data):
        """parse label structure

            "category" : {"label" : { "CA" : "Canada" }}
        :param json_data: json structure to parse
        """

        if self.__size is None:
            self.__size = len(json_data['label'])

        no_index = 'index' not in json_data
        if no_index:
            # self.__size = len(json_data['label'])
            self.__pos2cat = self.__size * [None]
            self.__idx2cat = {}

        self.__lbl2cat = {}

        for i, item in enumerate(json_data['label'].items()):
            idx = item[0]
            lbl = item[1]

            if no_index:
                # if index are not defined in json, give an order to the label
                pos = i
                cat = JsonStatCategory(pos=pos, label=lbl, index=idx)
            else:
                cat = self.__idx2cat.get(idx)
                if cat is None:
                    msg = "dimension '{}': label '{}' is associated with index '{}' that not exists!".format(self.__name, lbl, idx)
                    raise JsonStatMalformedJson(msg)
                pos = cat.pos
                cat = JsonStatCategory(pos=pos, label=lbl, index=idx)

            self.__pos2cat[pos] = cat
            # if only labels are present into the json,  deduce indexes from labels
            self.__idx2cat[idx] = cat
            self.__lbl2cat[lbl] = cat


if __name__ == "__main__":
    import doctest
    doctest.testmod()
