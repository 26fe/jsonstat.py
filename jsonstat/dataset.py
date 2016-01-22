# -*- coding: utf-8 -*-
# This file is part of jsonstat.py

# stdlib
from __future__ import print_function
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
        self.__valid = False
        self.__json_data = None

        self.__name = dataset_name
        self.__title = None
        self.__label = None
        self.__source = None

        self.__dimensions = {}
        self.__dimension_ids = None
        self.__dimension_sizes = None

        self.__value = None

    def from_file(self, filename):
        with open(filename) as f:
            json_string = f.read()
            self.from_string(json_string)

    def from_string(self, json_string):
        json_data = json.loads(json_string)
        self.from_json(json_data)

    def from_json(self, json_data, version=1):
        if version==2:
            self.__from_json_v2(json_data)
        else:
            self.__from_json_v1(json_data)

    def __from_json_v1(self, json_data):

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

        for dpos in range(len(self.__dimension_ids)):
            dname = self.__dimension_ids[dpos]
            dsize = self.__dimensions_sizes[dpos]
            # print "getting info for dimension '{}'".format(dname)

            if dname not in json_data_dimension:
                msg = "dataset '{}': malformed json: missing key {} in dimension".format(self.__name, dname)
                raise JsonStatException(msg)

            dimension = JsonStatDimension(dname, dsize, dpos, roles.get(dname))
            self.__dimensions[dname] = dimension
            dimension.from_json(json_data_dimension[dname])

    def name(self):
        return self.__name

    def __len__(self):
        return len(self.__value)

    def dimensions(self):
        return self.__dimensions.values()

    def dimension(self, dim):
        return self.__dimensions[dim]

    def info_dimensions(self):
        """
        print on stdout same info on dimensions
        """
        print("dimensions:")
        for i in range(len(self.__dimension_ids)):
            dname = self.__dimension_ids[i]
            d = self.__dimensions[dname]
            msg = "dim id/name: '{}' size: '{}' role: '{}'".format(d.name(), d.size(), d.role())
            print(msg)

    def info(self):
        """
        print ome info about this dataset on stdout
        """

        if self.__name is not None:
            print("name:   '{}'".format(self.__name))

        if self.__title is not None:
            print("title:  '{}'".format(self.__title))

        if self.__label is not None:
            print("label:  '{}'".format(self.__label))

        if self.__source is not None:
            print("source: '{}'".format(self.__label, self.__source))

        print("")
        self.info_dimensions()

    def value(self, **dims):
        """
        get a value
        :param dims:
        :return: value (typically a number)
        """
        if not self.__valid:
            raise JsonStatException('dataset not initialized')

        # print "-----------value"
        a = len(self.__dimension_ids) * [0]
        for d in dims.items():
            cat = d[0]
            val = d[1]
            dim = self.__dimensions[cat]
            a[dim.pos()] = dim.idx2pos(val)
            # print "{} -> {}".format(d, dim.position(val))

        return self.value_from_vec_pos(a)

    def value_from_vec_pos(self, lst):
        s = np.array(self.mult_vector)
        r = s * lst
        p = np.sum(r)
        # print "pos vector {} * mult vect {} = {} ({})".format(a, self.mult_vector,r,p)
        return self.__value[p]

    def from_vec_pos_to_vec_idx(self,vec_pos):
        vec_idx = len(vec_pos) * [None]
        for i in range(len(vec_pos)):
            dname = self.__dimension_ids[i]
            d = self.__dimensions[dname]
            vec_idx[i] = d.pos2idx(vec_pos[i])
        return vec_idx

    def from_vec_pos_to_vec_label(self,vec_pos):
        vec_idx = len(vec_pos) * [None]
        for i in range(len(vec_pos)):
            dname = self.__dimension_ids[i]
            d = self.__dimensions[dname]

            lbl = d.pos2label(vec_pos[i])
            if lbl is None:
                lbl = d.pos2idx(vec_pos[i])
            vec_idx[i] = lbl
        return vec_idx

    def all_pos(self, **dims):

        vec_pos_blocked = len(self.__dimension_ids) * [False]
        vec_pos = len(self.__dimension_ids) * [0]

        for d in dims.items():
            cat = d[0]
            idx = d[1]
            d = self.__dimensions[cat]
            vec_pos_blocked[d.pos()] = True
            vec_pos[d.pos()] = d.idx2pos(idx)

        nrd = 0
        while nrd < len(self.__dimensions_sizes):

            yield list(vec_pos)  # make a shallow copy of vec_pos

            nrd = 0
            # se la posizione non e bloccata allora puoi far andare avanti la cifra
            if not vec_pos_blocked[nrd]:
                vec_pos[nrd] += 1

            # se si arrivati al massimo valore o se la cifra e bloccata
            while nrd < len(self.__dimensions_sizes) and \
                    (vec_pos[nrd] == self.__dimensions_sizes[nrd] or vec_pos_blocked[nrd]):

                # se la posizione non e' bloccata allora puoi far partire il valore dall'inizio
                if not vec_pos_blocked[nrd]:
                    vec_pos[nrd] = 0

                # esamina la prossima posizione
                nrd += 1
                if nrd < len(self.__dimensions_sizes) and not vec_pos_blocked[nrd]:
                    vec_pos[nrd] += 1

    def generate_all_vec(self, **dims):
        for vec_pos in self.all_pos(**dims):
            vec_idx = self.from_vec_pos_to_vec_idx(vec_pos)
            value = self.value_from_vec_pos(vec_pos)
            # print "{} - {} -> {}".format(vec_pos, vec_idx, value)

    def to_table(self, content="label"):
        """
        Transforms a dataset into a table
        content could be "label" or "id"
        """
        table = []
        header = []

        if content == "label":
            for dname in self.__dimension_ids:
                header.append(self.__dimensions[dname].label())
        else:
            header = list(self.__dimension_ids)

        header.append("Value")
        table.append(header)
        for vec_pos in self.all_pos():
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

        index_pos = self.__dimensions[index].pos()
        columns = []
        for d in dims.items():
            cat = d[0]
            idx = d[1]
            columns.append(d[1])
        indexes = []
        values = []
        for vec_pos in self.all_pos(**dims):
            vec_idx = self.from_vec_pos_to_vec_idx(vec_pos)
            value = self.value_from_vec_pos(vec_pos)
            indexes.append(vec_idx[index_pos])
            values.append(value)
            # print "{} - {} -> {}".format(vec_pos, vec_idx, value)

        df = pd.DataFrame(values,
                          columns=columns,
                          index=indexes)

        return df



