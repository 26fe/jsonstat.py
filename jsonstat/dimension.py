# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import json

# jsonstat
from jsonstat.exceptions import JsonStatException
from jsonstat.exceptions import JsonStatMalformedJson


class JsonStatDimension:
    """
    Represents a JsonStat Dimension. It is contained into a JsonStat Dataset.
    """
    def __init__(self, name=None, size=None, pos=None, role=None):
        """initialize a dimension

        :param name: name of dimension
        :param size: size of dimension (nr of values)
        :param pos: position of dimension into the dataset
        :param role: of dimension
        """

        self.__valid = False

        self.__name = name
        self.__size = size
        self.__role = role
        self.__pos = pos
        self.__label = None

        # if indexes are not present in json __pos2idx will be None
        # if labels  are not present in json __pos2lbl will be None
        self.__pos2idx = None
        self.__pos2lbl = None

        self.__idx2pos = {}
        self.__idx2lbl = {}
        self.__lbl2idx = {}
        self.__lbl2pos = {}

    def name(self):
        """name of dimension"""
        return self.__name

    def label(self):
        """label of this dimension"""
        return self.__label

    # def size(self):
    #     """size of this dimension"""
    #     return self.__size

    def __len__(self):
        """size of this dimension"""
        return self.__size

    def pos(self):
        """position of this dimension respect to the dataset which dimension belongs to"""
        return self.__pos

    def role(self):
        """role of this dimension (time, geo or metric)"""
        return self.__role

    def idx2pos(self, idx):
        """
        from index to position
        :param idx: index for ex.: "2013"
        :return: integer
        """
        if not self.__valid:
            raise JsonStatException("dimension '{}': is not initialized".format(self.__name))
        if idx not in self.__idx2pos:
            raise JsonStatException("dimension '{}': do not have index '{}'".format(self.__name, idx))
        return self.__idx2pos[idx]

    def lbl2pos(self, lbl):
        """
        from label to position
        :param lbl: index for ex.: "2013"
        :return: integer
        """
        if not self.__valid:
            raise JsonStatException("dimension '{}': is not initialized".format(self.__name))
        if lbl not in self.__idx2pos:
            raise JsonStatException("dimension '{}': do not have label {}".format(self.__name, lbl))
        return self.__lbl2pos[lbl]

    def idx_or_lbl_2pos(self, idx_or_lbl):
        """
        from index to position
        :param idx_or_lbl:
        :param idx: index for ex.: "2013"
        :return: integer
        """
        if not self.__valid:
            raise JsonStatException("dimension {} is not initialized".format(self.__name))
        if idx_or_lbl in self.__idx2pos:
            return self.__idx2pos[idx_or_lbl]
        if idx_or_lbl in self.__lbl2pos:
            return self.__lbl2pos[idx_or_lbl]
        raise JsonStatException("dimension '{}': do not have index or label '{}'".format(self.__name, idx_or_lbl))

    def pos2idx(self, pos):
        """
        from position (integer) to index
        :param pos: integer
        :return: index f.e. "2013"
        """
        return self.__pos2idx[pos]

    def pos2label(self, pos):
        """
        get the label associated with the position
        :param pos: integer
        :return: the label or None if the label not exists at position pos
        """
        if self.__pos2lbl is None:
            return None
        else:
            return self.__pos2lbl[pos]

    def get_index(self):
        """
        get the index
        :return: a list of value
        """
        return list(self.__pos2idx)

    def __str__(self):
        out = "index\n"
        f = "{:>5} {:<8} {:<8}\n"
        out += f.format('pos', 'idx', 'label')
        for p in range(len(self.__pos2idx)):
            idx = self.__pos2idx[p]
            lbl = self.pos2label(p)
            if idx is None: idx = ""
            if lbl is None: lbl = ""

            out += f.format(p, "'" + idx + "'", "'" + lbl + "'")
        return out

    def __repr__(self):
        """
        used by ipython to make a better representation
        """
        return self.__str__()

    def info(self):
        """
        print some info on standard output about this dimension
        """
        print(self)

    #
    # parsing methods
    #

    def from_string(self, json_string):
        """
        Parse a json string
        :param json_string:
        :return itself to chain call
        """
        json_data = json.loads(json_string)
        self.from_json(json_data)
        return self

    def from_json(self, json_data):
        """
        Parse a json structure representing a dimensionid
        https://json-stat.org/format/#dimensionid
        :param json_data:
        :return itself to chain call
        """
        # children category, label, class
        if 'label' in json_data:
            self.__label = json_data['label']

        if 'class' in json_data:
            if json_data['class'] != 'dimension':
                msg = "class must be equals to 'dimension'"
                raise JsonStatMalformedJson(msg)

        # parsing category
        # category is required
        # https://json-stat.org/format/#category
        if "category" not in json_data:
            msg = "dimension '{}': missing category key".format(self.__name)
            raise JsonStatMalformedJson(msg)

        json_data_category = json_data['category']

        # children of category index, label, child, coordinates, unit
        # TODO: parse 'unit'
        if 'index' in json_data_category:
            self.__parse_json_index(json_data_category)

        if 'label' in json_data_category:
            self.__parse_json_label(json_data_category)

        # validate: label or index must be present
        if self.__pos2lbl is None and self.__pos2idx is None:
            msg = "dimension '{}': one of keys 'label' or 'index' must be presents"
            raise JsonStatMalformedJson(msg)

        # if only labels are present into the json deduce indexes from labels
        if self.__pos2idx is None:
            # preallocate a list of length self.size with default value None
            self.__pos2idx = self.__size * [None]
            for pos, lbl in enumerate(self.__pos2lbl):
                idx = self.__lbl2idx[lbl]
                self.__pos2idx[pos] = idx
                self.__lbl2pos[lbl] = pos
                self.__idx2pos[idx] = pos
                self.__idx2lbl[idx] = lbl

        # validate: number of indexes and labels must the same??
        if len(self.__idx2pos) > 0 and len(self.__lbl2idx) > 0:
            if len(self.__idx2pos) != len(self.__lbl2idx):
                # TODO: warning see hierarchy.json
                msg = "dimension '{}': the number of indexes ({}) are different of the numbers of labels ({})"
                msg = msg.format(self.__name, len(self.__idx2pos), len(self.__lbl2idx))
                # raise JsonStatMalformedJson(msg)
            if len(self.__idx2pos) < len(self.__lbl2idx):
                msg = "dimension '{}': the number of labels ({}) are greater than number of indexes ({})"
                msg = msg.format(self.__name, len(self.__lbl2idx), len(self.__idx2pos))
                raise JsonStatMalformedJson(msg)

        # validate: indexes must be consistent with size
        if self.__size != len(self.__idx2pos):
            msg = "dimension '{}': malformed json: number of indexes {} not match with size {}"
            msg = msg.format(self.__name, len(self.__idx2pos), self.__size)
            raise JsonStatMalformedJson(msg)

        # validate: no hole in the indexes
        if any(v is None for v in self.__pos2idx):
            msg = 'hole in index'
            raise JsonStatMalformedJson(msg)

        self.__valid = True
        return self

    def __parse_json_index(self, json_data):
        """
        parse index json structure
        for ex. the json structure could be
        "category" : { "index" : { "2003" : 0, "2004" : 1, "2005" : 2, "2006" : 3 }
        :param json_data: json stucture
        """

        if self.__size is None:
            self.__size = len(json_data['index'])

        # preallocate a list of length self.size with default value None
        self.__pos2idx = self.__size * [None]

        if type(json_data['index']) is list:
            for pos, idx in enumerate(json_data['index']):
                self.__parse_json_index_helper(idx, pos)
        else:
            for item in json_data['index'].items():
                idx = item[0]
                pos = item[1]
                self.__parse_json_index_helper(idx, pos)

    def __parse_json_index_helper(self, idx, pos):
        if pos >= self.__size:
            msg = "index {} for dimension '{}' is greater than size {}".format(pos, self.__name, self.__size)
            raise JsonStatException(msg)
        self.__idx2pos[idx] = pos
        self.__pos2idx[pos] = idx

    def __parse_json_label(self, json_data):
        """
        parse label structure
            "category" : {"label" : { "CA" : "Canada" }}
        :param json_data: json structure to parse
        """

        if self.__size is None:
            self.__size = len(json_data['label'])

        # preallocate __pos2label
        self.__pos2lbl = self.__size * [None]
        for i, item in enumerate(json_data['label'].items()):
            idx = item[0]
            lbl = item[1]

            if self.__pos2idx is None:
                # if index are not defined in json, give an order to the label
                pos = i
            else:
                pos = self.__idx2pos.get(idx)
                if pos is None:
                    msg = "dimension '{}': label '{}' is associated with index '{}' that not exists!".format(self.__name, lbl, idx)
                    raise JsonStatMalformedJson(msg)

            self.__pos2lbl[pos] = lbl
            self.__idx2lbl[idx] = lbl
            self.__lbl2idx[lbl] = idx
            self.__lbl2pos[lbl] = pos
