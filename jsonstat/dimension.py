# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

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

    >>> from jsonstat import JsonStatDimension
    >>> json_string = '''{
    ...                    "label" : "concepts",
    ...                    "category" : {
    ...                       "index" : { "POP" : 0, "PERCENT" : 1 },
    ...                       "label" : { "POP" : "population",
    ...                                   "PERCENT" : "weight of age group in the population" }
    ...                    }
    ...                  }
    ... '''
    >>> dim = JsonStatDimension(did="concept", role="metric").from_string(json_string)
    >>> len(dim)
    2
    >>> dim.category(0).index
    'POP'
    >>> dim.category('POP').label
    'population'
    >>> dim.category(1)
    JsonStatCategory(label='weight of age group in the population', index='PERCENT', pos=1)
    >>> print(dim)
    +-----+-----------+-----------------------------------------+
    | pos | idx       | label                                   |
    +-----+-----------+-----------------------------------------+
    | 0   | 'POP'     | 'population'                            |
    | 1   | 'PERCENT' | 'weight of age group in the population' |
    +-----+-----------+-----------------------------------------+
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
    """

    def __init__(self, did=None, size=None, pos=None, role=None):
        """initialize a dimension

        .. warning::

            this is an internal library function (it is not public api)

        :param did: id of dimension
        :param size: size of dimension (nr of values)
        :param pos: position of dimension into the dataset
        :param role: of dimension
        """

        # it is valid if is correctly built (f.e. it was parsed correctly)
        self.__valid = False

        self.__did = did
        self.__size = size
        self.__role = role
        self.__pos = pos
        self.__label = None

        # if indexes are not present in json __idx2cat will be None
        # if labels  are not present in json __lbl2cat will be None
        self.__pos2cat = None  # int -> cat
        self.__idx2cat = None  # idx -> cat
        self.__lbl2cat = None  # lbl -> cat

    #
    # queries
    #   dimension properties

    @property
    def did(self):
        """id of this dimension"""
        return self.__did

    @property
    def label(self):
        """label of this dimension"""
        return self.__label

    @property
    def role(self):
        """role of this dimension (can be time, geo or metric)"""
        return self.__role

    @property
    def pos(self):
        """position of this dimension with respect to the data set to which this dimension belongs"""
        return self.__pos

    def __len__(self):
        """size of this dimension"""
        return self.__size

    def __to_list(self):
        lst = [["pos", "idx", "label"]]
        for cat in self.__pos2cat:
            idx = cat.index
            lbl = cat.label
            if idx is None: idx = ""
            if lbl is None: lbl = ""
            row = [str(cat.pos), "'" + idx + "'", "'" + lbl + "'"]
            row = list(map(lambda x: "" if x is None else x, row))
            lst.append(row)
        return lst

    def __str__(self):
        if self.__pos2cat is None:
            return ""

        lst = self.__to_list()

        table = terminaltables.AsciiTable(lst)
        out = table.table
        return out

    def __repr__(self):
        """used by ipython to make a better representation"""
        return self.__str__()

    def _repr_html_(self):
        lst = self.__to_list()
        html = "<table>"
        maxlines = 5
        nr_line = 0
        while nr_line < maxlines and nr_line < len(lst):
            l = lst[nr_line]
            html += "<tr>"
            for c in l:
                html += "<td>{}</td>".format(c)
            html += "</tr>"
            nr_line += 1
        if nr_line < len(lst):
            html += "<td>...</td>" * len(lst[0])
        html += "</table>"
        return html

    #
    # queries
    #   categories
    #

    def category(self, spec):
        """return JsonStatCategory according to spec

        :param spec: can be index (string) or label (string) or a position (integer)
        :returns: a JsonStatCategory
        """
        if not self.__valid:
            raise JsonStatException("dimension '{}': is not initialized".format(self.__did))

        if isinstance(spec, int) and spec < len(self.__pos2cat):
            cat = self.__pos2cat[spec]
            return cat

        # try first indexes
        if spec in self.__idx2cat:
            cat = self.__idx2cat[spec]
            return cat

        if self.__lbl2cat is not None and spec in self.__lbl2cat:
            cat = self.__lbl2cat[spec]
            return cat

        raise JsonStatException("dimension '{}': unknown index or label '{}'".format(self.__did, spec))

    def _pos2cat(self, pos):
        """get the category associated with the position (integer)

        :param pos: integer
        :returns: the label or None if the label not exists at position pos
            ex.: JsonStatCategory(index='2013', label='2013', pos=pos)
        """
        if not self.__valid:
            raise JsonStatException("dimension '{}': is not initialized".format(self.__did))
        if self.__pos2cat is None:
            return None
        return self.__pos2cat[pos]

    def _idx2pos(self, idx):
        """from index to position

        :param idx: index for ex.: "2013"
        :returns: integer
        """
        if not self.__valid:
            raise JsonStatException("dimension '{}': is not initialized".format(self.__did))
        if idx not in self.__idx2cat:
            raise JsonStatException("dimension '{}': do not have index '{}'".format(self.__did, idx))
        return self.__idx2cat[idx].pos

    def _lbl2pos(self, lbl):
        """from label to position

        :param lbl: index for ex.: "2013"
        :returns: integer
        """
        if not self.__valid:
            raise JsonStatException("dimension '{}': is not initialized".format(self.__did))
        if lbl not in self.__idx2cat:
            raise JsonStatException("dimension '{}': do not have label {}".format(self.__did, lbl))
        return self.__lbl2cat[lbl].pos

    #
    # parsing methods
    #

    def from_string(self, json_string):
        """parse a json string

        :param json_string:
        :returns: itself to chain calls
        """
        json_data = json.loads(json_string)
        self.from_json(json_data)
        return self

    def from_json(self, json_data):
        """Parse a json structure representing a dimension

        From `json-stat.org <https://json-stat.org/format/#dimensionid>`_

            It is used to describe a particular dimension.
            The name of this object must be one of the strings in the id array.
            There must be one and only one dimension ID object for every dimension in the id array.

        jsonschema for dimension is about::

            "dimension": {
                "type": "object",
                "properties": {
                    "version": {"$ref": "#/definitions/version"},
                    "href": {"$ref": "#/definitions/href"},
                    "class": {"type": "string", "enum": ["dimension"]},
                    "label": {"type": "string"},
                    "category": {"$ref": "#/definitions/category"},
                    "note": {"type": "array"},
                },
                "additionalProperties": false
            },

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
            msg = "dimension '{}': missing category key".format(self.__did)
            raise JsonStatMalformedJson(msg)

        self.__parse_category(json_data['category'])

        self.__valid = True
        return self

    def __parse_category(self, json_data_category):
        """It is used to describe the possible values of a dimension.
        See https://json-stat.org/format/#category
        :param json_data_category:
        :returns:

        jsonschema for dimension is about::

            "category": {
                "type": "object",
                "properties": {
                    "index": {"$ref": "#/definitions/category_index"},
                    "label": {"type": "object"},

                    "unit": {"$ref": "#/definitions/category_index"},
                    "child": {"type": "object", "properties": {"additionalProperties": {"type": "array"}}},
                    "coordinates": {"type": "object",
                                    "properties": {"additionalProperties": {"type": "array"}}},
                    "note": {"type": "array"}

                },
                "additionalProperties": false
            },

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
                # TODO: cannot raise exception, emit warning see hierarchy.json
                msg = "dimension '{}': the number of indexes ({}) are different of the numbers of labels ({})"
                msg = msg.format(self.__did, len(self.__idx2cat), len(self.__lbl2cat))
                # raise JsonStatMalformedJson(msg)
            if len(self.__idx2cat) < len(self.__lbl2cat):
                msg = "dimension '{}': the number of labels ({}) are greater than number of indexes ({})"
                msg = msg.format(self.__did, len(self.__lbl2cat), len(self.__idx2cat))
                raise JsonStatMalformedJson(msg)

        # validate: indexes must be consistent with size
        if self.__size != len(self.__idx2cat):
            msg = "dimension '{}': malformed json: number of indexes {} not match with size {}"
            msg = msg.format(self.__did, len(self.__idx2cat), self.__size)
            raise JsonStatMalformedJson(msg)

        # validate: no hole in the indexes
        if any(v is None for v in self.__pos2cat):
            msg = "dimension '{}':hole in index".format(self.__did)
            raise JsonStatMalformedJson(msg)

        # "category_unit": {
        #                      "type": "object",
        #                      "properties": {
        #                          "additionalProperties": {
        #                              "type": "object",
        #                              "properties": {"label": {"type": "string"},
        #                                             "decimals": {"type": "number"},
        #                                             "type": {"type": "string"},
        #                                             "base": {"type": "string"},
        #                                             "multiplier": {"type": "number"},
        #                                             "position": {"type": "string"}},
        #                              "additionalProperties": false
        #                          }
        #                      }
        #                  },

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
                msg = "dimension {}: 'unit' can be used only when role is 'metric'"
                msg = msg.format(self.__did)
                JsonStatException(msg)
            self.__unit = json_data_category['unit']

    def __parse_json_index(self, json_data):
        """parse index json structure

        for ex. the json structure could be
            "category" : { "index" : { "2003" : 0, "2004" : 1, "2005" : 2, "2006" : 3 }
        :param json_data: json structure
        """

        json_data_index = json_data['index']
        if self.__size is None:
            self.__size = len(json_data_index)

        self.__idx2cat = {}

        # preallocate a list of length self.size with default value None
        self.__pos2cat = self.__size * [None]

        if type(json_data_index) is list:
            for pos, idx in enumerate(json_data_index):
                self.__parse_json_index_helper(idx, pos)
        else:
            for idx, pos in json_data_index.items():
                self.__parse_json_index_helper(idx, pos)

    def __parse_json_index_helper(self, idx, pos):
        if pos >= self.__size:
            msg = "dimension '{}': index {} is greater than size {}"
            msg = msg.format(self.__did, pos, self.__size)
            raise JsonStatException(msg)

        cat = JsonStatCategory(pos=pos, index=idx, label=None)
        self.__pos2cat[pos] = cat
        self.__idx2cat[idx] = cat

    def __parse_json_label(self, json_data):
        """parse label structure

            "category" : {"label" : { "CA" : "Canada" }}
        :param json_data: json structure to parse
        """

        json_data_label = json_data['label']
        if self.__size is None:
            self.__size = len(json_data_label)

        no_index = 'index' not in json_data
        if no_index:
            # self.__size = len(json_data['label'])
            self.__pos2cat = self.__size * [None]
            self.__idx2cat = {}

        self.__lbl2cat = {}

        for i, (idx, lbl) in enumerate(json_data_label.items()):

            if no_index:
                # if index are not defined in json, give an order to the label
                pos = i
                cat = JsonStatCategory(pos=pos, label=lbl, index=idx)
            else:
                cat = self.__idx2cat.get(idx)
                if cat is None:
                    msg = "dimension '{}': label '{}' is associated with index '{}' that not exists!"
                    msg = msg.format(self.__did, lbl, idx)
                    raise JsonStatMalformedJson(msg)
                pos = cat.pos
                cat = JsonStatCategory(pos=pos, label=lbl, index=idx)

            self.__pos2cat[pos] = cat
            # if only labels are present into the json,  deduce indexes from labels
            self.__idx2cat[idx] = cat
            self.__lbl2cat[lbl] = cat
