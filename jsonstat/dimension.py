# -*- coding: utf-8 -*-
# This file is part of jsonstat.py

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
        :return:
        """

        self.__valid = False

        self.__name = name
        self.__size = size
        self.__role = role
        self.__pos = pos
        self.__label = None

        # preallocate a list of length self.size with default value None
        self.__from_pos_to_index = self.__size * [None]
        self.__from_pos_to_label = self.__size * [None]

        self.__from_index_to_pos = {}
        self.__from_label_to_index = {}
        self.__from_index_to_label = {}

    def from_string(self, json_string):
        """Parse a json string
        :param json_string:
        """
        json_data = json.loads(json_string)
        self.from_json(json_data)

    def from_json(self, json_data):
        """Parse a json structure
        :param json_data:
        :return:
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
            # msg = "missing 'index' key in dimension '{}'".format(self.name)
            # raise JsonStatMalformedJson(msg)

        if 'label' in json_data_category:
            self.__parse_json_label(json_data_category)

        # check if from_index_to_pos is empty
        # MAYBE from_index_to_pos is empty only on dimension of size 1
        if len(self.__from_index_to_pos) == 0:
            pos = 0
            for idx in self.__from_label_to_index.values():
                self.__from_index_to_pos[idx] = pos
                self.__from_pos_to_index[pos] = idx
                pos += 1

        if len(self.__from_index_to_pos) > 0 and len(self.__from_label_to_index) > 0:
            if len(self.__from_index_to_pos) != len(self.__from_label_to_index):
                msg = "dimension '{}': mismatch between indexes {} and labels {}"
                msg = msg.format(self.__name, len(self.__from_index_to_pos), len(self.__from_label_to_index))
                raise JsonStatMalformedJson(msg)

        if self.__size != len(self.__from_index_to_pos):
            msg = "dimension '{}': malformed json: number of category {} not match with size {}"
            msg = msg.format(self.__name, len(self.__from_index_to_pos), self.__size)
            raise JsonStatMalformedJson(msg)

        if any(v is None for v in self.__from_pos_to_index):
            msg = 'hole in index'
            raise JsonStatMalformedJson(msg)

        self.__valid = True

        # parse json index structure

    # "category" : { "index" : { "2003" : 0, "2004" : 1, "2005" : 2, "2006" : 3 }
    def __parse_json_index(self, json_data_category):
        if type(json_data_category['index']) is list:
            for i in json_data_category['index']:
                pass
                # print i
        else:
            for i in json_data_category['index'].items():
                # print i
                cat = i[0]
                idx = i[1]
                if idx >= self.__size:
                    msg = "index {} for dimension '{}' is greater than size {}".format(idx, self.__name, self.__size)
                    raise JsonStatException(msg)
                self.__from_index_to_pos[cat] = idx
                self.__from_pos_to_index[idx] = cat

    def __parse_json_label(self, json_data_category):
        """parse label structure
            "category" : {"label" : { "CA" : "Canada" }}
        :param json_data_category:
        :return:
        """
        for i in json_data_category['label'].items():
            idx = i[0]
            lbl = i[1]

            pos = self.__from_index_to_pos.get(idx)
            if pos is not None:
                self.__from_pos_to_label[pos] = lbl

            self.__from_index_to_label[idx] = lbl
            self.__from_label_to_index[lbl] = idx

    def name(self):
        """

        :return:
        """
        return self.__name

    def label(self):
        """

        :return:
        """
        return self.__label

    def size(self):
        return self.__size

    def __len__(self):
        return self.__size

    def pos(self):
        return self.__pos

    def role(self):
        return self.__role

    def idx2pos(self, idx):
        """from index to position

        :param idx:
        :return:
        """
        if not self.__valid:
            raise JsonStatException("dimension not initialized")
        return self.__from_index_to_pos[idx]

    def pos2idx(self, pos):
        """from position (integer) to index
        :param pos:
        :return:
        """
        return self.__from_pos_to_index[pos]

    def pos2label(self, pos):
        """from the position get the label
        :param pos: integer
        :return: the label
        """
        return self.__from_pos_to_label[pos]

    def get_index(self):
        """
        get the index
        :return: a list of value
        """
        return list(self.__from_pos_to_index)

    def __str__(self):
        out = "index\n"
        f = "{:>5} {:>6} {:>6}\n"
        out += f.format('pos', 'idx', 'label')
        for p in range(len(self.__from_pos_to_index)):
            idx = self.__from_pos_to_index[p]
            if idx is None:
                idx = ""

            lbl = self.__from_pos_to_label[p]
            if lbl is None:
                lbl = ""

            out += f.format(p, idx, lbl)
        return out

    def info(self):
        """
        print some info on standard output about this dimension
        """
        print(self)
