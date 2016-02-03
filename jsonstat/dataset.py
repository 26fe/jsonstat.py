# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
from functools import reduce
import json

# packages
import numpy as np
import pandas as pd

# jsonstat
from jsonstat.dimension import JsonStatDimension
from jsonstat.exceptions import JsonStatException
from jsonstat.exceptions import JsonStatMalformedJson


class JsonStatDataSet:
    """
    Represents a Dataset
    """
    def __init__(self, dataset_name=None):
        """
        Initialize a empty dataset. If we are parsing jsonstat version 1, the dataset has a name.
        :param dataset_name: dataset name (jsonstat v.1)
        """
        self.__valid = False
        self.__json_data = None

        self.__name = dataset_name
        self.__title = None
        self.__label = None
        self.__source = None

        self.__id2dimension = {}
        self.__dimensions = []
        self.__dimension_ids = None
        self.__dimension_sizes = None

        self.__value = None

    def name(self):
        """
        Returns the name of the dataset
        """

        return self.__name

    def __len__(self):
        """
        size of the dataset
        :return:
        """
        return len(self.__value)

    def dimensions(self):
        """
        :return: list of JsonStatDimension
        """
        return self.__dimensions

    def dimension(self, spec):
        """
        get a dimension by spec
        :param spec: name of the dimension
        :return: a JsonStatDimension
        """
        return self.__id2dimension[spec]

    def __str__dimensions(self):
        out = "{} dimensions:\n".format(len(self.__dimension_ids))
        for i, dname in enumerate(self.__dimension_ids):
            d = self.__id2dimension[dname]
            out += "  {}: dim id/name: '{}' size: '{}' role: '{}'\n".format(i, d.name(), d.size(), d.role())
        return out

    def info_dimensions(self):
        """
        print on stdout same info on dimensions
        """
        print(self.__str__dimensions())

    def __str__(self):
        out = ""
        if self.__name is not None:
            out += "name:   '{}'\n".format(self.__name)

        if self.__title is not None:
            out += "title:  '{}'\n".format(self.__title)

        if self.__label is not None:
            out += "label:  '{}'\n".format(self.__label)

        if self.__source is not None:
            out += "source: '{}'\n".format(self.__label, self.__source)

        out += "size: {}".format(len(self))
        out += "\n"
        out += self.__str__dimensions()
        return out

    def __repr__(self):
        """
        used by ipython to make a better representation
        """
        return self.__str__()

    def info(self):
        """
        print ome info about this dataset on stdout
        """
        print(self)

    def value(self, **dims):
        """
        get a value
        :param dims:
        :return: value (typically a number)
        """
        if not self.__valid:
            raise JsonStatException('dataset not initialized')

        a = len(self.__dimension_ids) * [0]
        for d in dims.items():
            cat = d[0]
            val = d[1]
            dim = self.__id2dimension[cat]
            a[dim.pos()] = dim.idx2pos(val)
            # print "{} -> {}".format(d, dim.position(val))

        return self.value_from_vec_pos(a)

    def value_from_vec_pos(self, lst):
        """
        :param lst: [0,3,4]
        :return: value at dimension [0,3,4]
        """
        s = np.array(self.mult_vector)
        r = s * lst
        p = np.sum(r)
        # print "pos vector {} * mult vect {} = {} ({})".format(a, self.mult_vector,r,p)
        return self.__value[p]

    def from_vec_pos_to_vec_idx(self, vec_pos):
        """
        :param vec_pos:  [0,3,4]
        :return: ['dimension 1 index', 'dimension 2 label', 'dimension 3 label']
        """
        vec_idx = len(vec_pos) * [None]
        for i in range(len(vec_pos)):
            dname = self.__dimension_ids[i]
            d = self.__id2dimension[dname]
            vec_idx[i] = d.pos2idx(vec_pos[i])
        return vec_idx

    def from_vec_pos_to_vec_label(self, vec_pos):
        """
        :param vec_pos:  [0,3,4]
        :return: ['dimension 1 label or index', 'dimension 2 label  or index', 'dimension 3 label  or index']
        """
        vec_idx = len(vec_pos) * [None]
        for i in range(len(vec_pos)):
            dname = self.__dimension_ids[i]
            d = self.__id2dimension[dname]

            lbl = d.pos2label(vec_pos[i])
            if lbl is None:
                lbl = d.pos2idx(vec_pos[i])

            vec_idx[i] = lbl
        return vec_idx

    def from_vec_idx_to_vec_dim(self, lst_ids):
        """
        From a list of dimension name to a list of numerical dimension position
         F.e.
         ["year", "country"] -> [1,0]
         ["country", "year"] -> [0,1]
        :return: list of number
        """
        return [self.__id2dimension[iid].pos() for iid in lst_ids]


    def all_pos(self, block_dim = {}, order=None):
        """

        :param block_dim:  {"year":2013, country:"IT"}
        :return:
        """

        ids = self.__dimension_ids

        vec_pos_blocked = len(ids) * [False]
        vec_pos = len(ids) * [0]             # [0,0,0]

        for d in block_dim.items():
            cat = d[0]
            idx = d[1]
            d = self.__id2dimension[cat]
            vec_pos_blocked[d.pos()] = True
            vec_pos[d.pos()] = d.idx2pos(idx)

        dsizes = self.__dimensions_sizes
        max_dimensions = len(dsizes)

        if order is None:
            vec_dimension_reorder = range(len(ids))
        else:
            vec_dimension_reorder = order

        nrd = 0
        while nrd < max_dimensions:

            yield list(vec_pos)  # make a shallow copy of vec_pos

            nrd = 0
            current_dimension = vec_dimension_reorder[nrd]
            # se la posizione non e bloccata allora puoi far andare avanti la cifra
            if not vec_pos_blocked[current_dimension]:
                vec_pos[current_dimension] += 1

            # se non si arrivati all'ultima dimensione
            # e se la dimensione corrente non e al massimo valore o se la dimensione corrente e bloccata
            while nrd < max_dimensions and \
                    (vec_pos[current_dimension] == dsizes[current_dimension] or vec_pos_blocked[current_dimension]):

                # se la posizione non e' bloccata allora puoi far partire il valore dall'inizio
                if not vec_pos_blocked[current_dimension]:
                    vec_pos[current_dimension] = 0

                # esamina la prossima posizione
                nrd += 1
                # se la dimensione corrente non e' l'ultima
                if nrd < max_dimensions:
                    current_dimension = vec_dimension_reorder[nrd]
                    # se la dimensione corrente non e bloccata puoi farla avanzare
                    if not vec_pos_blocked[current_dimension]:
                        vec_pos[current_dimension] += 1

    def generate_all_vec(self, **dims):
        for vec_pos in self.all_pos(dims):
            vec_idx = self.from_vec_pos_to_vec_idx(vec_pos)
            value = self.value_from_vec_pos(vec_pos)
            # print "{} - {} -> {}".format(vec_pos, vec_idx, value)

    #
    # transforming function
    #
    def to_table(self, content="label", order=None):
        """
        Transforms a dataset into a table (a list of row)
        table len is the size of dataset + 1 for headers
        :param content can be "label" or "id"
        return: a list of row, fist line is the header
        """
        table = []

        # header
        header = []
        if content == "label":
            for dname in self.__dimension_ids:
                header.append(self.__id2dimension[dname].label())
        else:
            header = list(self.__dimension_ids)

        header.append("Value")

        # data
        table.append(header)
        for vec_pos in self.all_pos(order=order):
            value = self.value_from_vec_pos(vec_pos)
            if content == "label":
                row = self.from_vec_pos_to_vec_label(vec_pos)
            else:
                row = self.from_vec_pos_to_vec_idx(vec_pos)
            row.append(value)
            table.append(row)

        return table

    def to_data_frame(self, index, **dims):
        """
        extract a bidimensional table
              col ->
         row

        extract_bidimensional("year", "country")
        generate the following dataframe:
        year  |  country
        2010  |  1
        2011  |  2
        2012  |  3

        :param index:
        :param dims:
        :return:
        """

        index_pos = self.__id2dimension[index].pos()
        columns = []
        for d in dims.items():
            cat = d[0]
            idx = d[1]
            columns.append(d[1])
        indexes = []
        values = []
        for vec_pos in self.all_pos(dims):
            vec_idx = self.from_vec_pos_to_vec_idx(vec_pos)
            value = self.value_from_vec_pos(vec_pos)
            indexes.append(vec_idx[index_pos])
            values.append(value)
            # print "{} - {} -> {}".format(vec_pos, vec_idx, value)

        df = pd.DataFrame(values,
                          columns=columns,
                          index=indexes)

        return df

    #
    # Parsing code
    #

    def from_file(self, filename):
        """
        read a jsonstat from a file and parse it to inizialize this (empty) dataset
        :param filename: path of the file.
        :return itself to chain call
        """
        with open(filename) as f:
            json_string = f.read()
            self.from_string(json_string)
        return self

    def from_string(self, json_string):
        """
        parse a string to inizialize this (empty) dataset
        :param json_string:
        :return itself to chain call
        """

        json_data = json.loads(json_string)
        self.from_json(json_data)
        return self

    def from_json(self, json_data, version=1):
        """

        :param json_data:
        :param version:
        :return itself to chain call
        """
        if version == 2:
            self.__from_json_v2(json_data)
        else:
            self.__from_json_v1(json_data)
        return self

    def __from_json_v1(self, json_data):
        """
        parse jsonstat format version 1
        :param json_data: json structure
        """

        self.__json_data = json_data

        if 'label' in json_data:
            self.__label = json_data['label']
            if self.__name is None:
                self.__name = self.__label

        if 'value' not in json_data:
            msg = "dataset '{}': missing 'value' key".format(self.__name)
            raise JsonStatMalformedJson(msg)
        if 'dimension' not in json_data:
            msg = "dataset '{}': missing 'dimension' key".format(self.__name)
            raise JsonStatMalformedJson(msg)

        json_data_dimension = json_data['dimension']
        if 'id' not in json_data_dimension:
            msg = "dataset '{}': missing 'dimension.id' key".format(self.__name)
            raise JsonStatMalformedJson(msg)
        if 'size' not in json_data_dimension:
            msg = "dataset '{}': missing 'dimension.size' key".format(self.__name)
            raise JsonStatMalformedJson(msg)

        if 'source' in json_data:
            self.__source = json_data['source']

        if 'title' in json_data:
            self.__title = json_data['title']

        self.__parse_dimensions(json_data_dimension)

        self.__value = json_data['value']
        if len(self.__value) == 0:
            msg = "dataset '{}': value is empty".format(self.__name)
            raise JsonStatMalformedJson(msg)

        size_total = reduce(lambda x, y: x * y, self.__dimensions_sizes)
        if len(self.__value) != size_total:
            msg = "dataset '{}': size {} is different from calculate size {} by dimension"
            msg = msg.format(self.__name, len(self.__value), size_total)
            raise JsonStatMalformedJson(msg)

        self.__valid = True

    def __from_json_v2(self, json_data):
        """
        parse jsonstat format version 1
        :param json_data: json structure
        """
        pass

    def __parse_dimensions(self, json_data_dimension):

        self.__dimension_ids = json_data_dimension['id']
        self.__dimensions_sizes = json_data_dimension['size']

        if len(self.__dimension_ids) != len(self.__dimensions_sizes):
            msg = "dataset '{}': dataset_id is different of dataset_size".format(self.__name)
            raise JsonStatMalformedJson(msg)

        acc = 1
        self.mult_vector = [1]
        for i in range(1, len(self.__dimensions_sizes)):
            acc = acc * self.__dimensions_sizes[i - 1]
            self.mult_vector.append(acc)

        roles = {}
        if 'role' in json_data_dimension:
            json_roles = json_data_dimension['role']
            for r in json_roles.items():
                role = r[0]
                for dname in r[1]:
                    # print "{} -> {}".format(dname, role)
                    roles[dname] = role

        self.__dimensions = len(self.__dimension_ids) * [None]
        for dpos in range(len(self.__dimension_ids)):
            dname = self.__dimension_ids[dpos]
            dsize = self.__dimensions_sizes[dpos]
            # print "getting info for dimension '{}'".format(dname)

            if dname not in json_data_dimension:
                msg = "dataset '{}': malformed json: missing key {} in dimension".format(self.__name, dname)
                raise JsonStatException(msg)

            dimension = JsonStatDimension(dname, dsize, dpos, roles.get(dname))
            self.__id2dimension[dname] = dimension
            self.__dimensions[dpos] = dimension
            dimension.from_json(json_data_dimension[dname])

