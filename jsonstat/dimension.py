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
    Represents a JsonStatDimension. It is contained into a Dataset.
    """
    def __init__(self, name, size, pos, role):
        """
        initialize a dimension
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

        # if indexes are not present in json __pos2index will be None
        # if labels  are not present in json __pos2label will be None
        self.__pos2index = None
        self.__pos2label = None

        self.__index2pos = {}
        self.__label2index = {}
        self.__index2label = {}

    def name(self):
        """
        name of dimension
        """
        return self.__name

    def label(self):
        """
        label of this dimenion
        """
        return self.__label

    def size(self):
        """
        size of this dimension
        """
        return self.__size

    def __len__(self):
        """
        len of this dimesion (the same of the size)
        """
        return self.__size

    def pos(self):
        """
        position of this dimension respect to the dataset which dimension belongs to
        """
        return self.__pos

    def role(self):
        return self.__role

    def idx2pos(self, idx):
        """
        from index to position

        :param idx:
        :return:
        """
        if not self.__valid:
            raise JsonStatException("dimension {} is not initialized".format(self.__name))
        if idx not in self.__index2pos:
            raise JsonStatException("dimension {} do not have index {}".format(self.__name, idx))
        return self.__index2pos[idx]

    def pos2idx(self, pos):
        """
        from position (integer) to index
        :param pos:
        :return:
        """
        return self.__pos2index[pos]

    def pos2label(self, pos):
        """
        get the label associaate with the position
        :param pos: integer
        :return: the label or None if the label not exists at position pos
        """
        if self.__pos2label is None:
            return None
        else:
            return self.__pos2label[pos]

    def get_index(self):
        """
        get the index
        :return: a list of value
        """
        return list(self.__pos2index)

    def __str__(self):
        out = "index\n"
        f = "{:>5} {:>6} {:>6}\n"
        out += f.format('pos', 'idx', 'label')
        for p in range(len(self.__pos2index)):
            idx = self.__pos2index[p]
            lbl = self.pos2label(p)
            if idx is None: idx = ""
            if lbl is None: lbl = ""

            out += f.format(p, idx, lbl)
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
        """Parse a json structure
        :param json_data:
        :return itself to chain call
        """
        if 'label' in json_data:
            self.__label = json_data['label']

        # parse category
        if "category" not in json_data:
            msg = "dimension '{}': missing category key".format(self.__name)
            raise JsonStatMalformedJson(msg)

        json_data_category = json_data['category']

        if 'index' in json_data_category:
            self.__parse_json_index(json_data_category)

        if 'label' in json_data_category:
            self.__parse_json_label(json_data_category)

        if self.__pos2label is None and self.__pos2index is None:
            msg = "dimension '{}': one of keys 'label' or 'category' must be presents"
            raise JsonStatMalformedJson(msg)

        # check if from_index_to_pos is empty
        # MAYBE from_index_to_pos is empty only on dimension of size 1
        # if len(self.__index2pos) == 0:
        #     pos = 0
        #     for idx in self.__label2index.values():
        #         self.__index2pos[idx] = pos
        #         self.__pos2index[pos] = idx
        #         pos += 1

        # if only labels are present into the json
        # initialize structures for manage indexes
        if self.__pos2index is None:
            # preallocate a list of length self.size with default value None
            self.__pos2index = self.__size * [None]
            for pos, lbl in enumerate(self.__pos2label):
                idx = self.__label2index[lbl]
                self.__pos2index[pos] = idx
                self.__index2pos[idx] = pos
                self.__index2label[idx] = lbl

        if len(self.__index2pos) > 0 and len(self.__label2index) > 0:
            if len(self.__index2pos) != len(self.__label2index):
                msg = "dimension '{}': mismatch between indexes {} and labels {}"
                msg = msg.format(self.__name, len(self.__index2pos), len(self.__label2index))
                raise JsonStatMalformedJson(msg)

        if self.__size != len(self.__index2pos):
            msg = "dimension '{}': malformed json: number of indexes {} not match with size {}"
            msg = msg.format(self.__name, len(self.__index2pos), self.__size)
            raise JsonStatMalformedJson(msg)

        if any(v is None for v in self.__pos2index):
            msg = 'hole in index'
            raise JsonStatMalformedJson(msg)

        self.__valid = True
        return self

    def __parse_json_index(self, json_data):
        """
        parse index json structure
        for ex. the json strcuture could be
        "category" : { "index" : { "2003" : 0, "2004" : 1, "2005" : 2, "2006" : 3 }
        :param json_data:
        """

        # preallocate a list of length self.size with default value None
        self.__pos2index = self.__size * [None]
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
        self.__index2pos[idx] = pos
        self.__pos2index[pos] = idx

    def __parse_json_label(self, json_data):
        """
        parse label structure
            "category" : {"label" : { "CA" : "Canada" }}
        :param json_data: json structure to parse
        """

        # preallocate __pos2label
        self.__pos2label = self.__size * [None]
        for i, item in enumerate(json_data['label'].items()):
            idx = item[0]
            lbl = item[1]

            if self.__pos2index is None:
                # if index are not defined in json, give an order to the label
                self.__pos2label[i] = lbl
            else:
                pos = self.__index2pos.get(idx)
                if pos is None:
                    msg = "dimension '{}': label '{}' is associated with index '{}' that not exists!".format(self.__name, lbl, idx)
                    raise JsonStatMalformedJson(msg)
                self.__pos2label[pos] = lbl

            self.__index2label[idx] = lbl
            self.__label2index[lbl] = idx
