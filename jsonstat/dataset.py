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
    Represents a JsonStat dataset
    """

    def __init__(self, dataset_name=None):
        """
        Initialize an empty dataset.
        Dataset could have a name if we parse a jsonstat format version 1.
        :param dataset_name: dataset name (jsonstat v.1)
        """
        self.__valid = False
        self.__json_data = None

        self.__name = dataset_name
        self.__title = None
        self.__label = None
        self.__source = None

        self.__id2pos = {}
        self.__dim_nr = 0
        self.__pos2dim = []
        self.__dim_ids = None
        self.__dimension_sizes = None

        self.__value = None

    def name(self):
        """
        Returns the name of the dataset
        """
        return self.__name

    def __len__(self):
        """
        :return: size of the dataset
        """
        return len(self.__value)

    def dimensions(self):
        """
        :return: list of JsonStatDimension
        """
        return self.__pos2dim

    def dimension(self, spec):
        """
        get a dimension by spec
        :param spec: name (string) or id of the dimension
        :return: a JsonStatDimension
        """
        if type(spec) is int:
            return self.__pos2dim[spec]
        if spec not in self.__id2pos:
            msg = "dataset '{}': unknown dimension '{}' know dimensions ids are: {}".format(self.__name, spec, ", ".join(self.__dim_ids))
            raise JsonStatException(msg)
        return self.__id2pos[spec]

    def __str__dimensions(self):
        out = "{} dimensions:\n".format(len(self.__dim_ids))
        for i, dname in enumerate(self.__dim_ids):
            d = self.__id2pos[dname]
            out += "  {}: dim id/name: '{}' size: '{}' role: '{}'\n".format(i, d.name(), d.size(), d.role())
        return out

    def info_dimensions(self):
        """
        print same info on dimensions on stdout
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

    #
    # from function
    #

    def value(self, **dims):
        """
        get a value
        :param dims: {country:"AU", "year":"2014:}
        :return: value (typically a number)
        """
        if not self.__valid:
            raise JsonStatException('dataset not initialized')

        a = self.from_vec_dim_to_vec_pos(dims)
        return self.value_from_vec_pos(a)

    def from_vec_dim_to_vec_pos(self, dims):
        """

        :param dims: {country:"AU", "year":2014}
        :return: [1,2,3]
        """
        vec_pos = len(self.__dim_ids) * [0]
        for d in dims.items():
            cat = d[0]
            val = d[1]
            dim = self.__id2pos[cat]
            vec_pos[dim.pos()] = dim.idx2pos(val)
        return vec_pos

    def value_from_vec_pos(self, lst):
        """
        :param lst: [0,3,4]
        :return: value at dimension [0,3,4]
        """
        s = np.array(self.__acc_vector)
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
            dname = self.__dim_ids[i]
            d = self.__id2pos[dname]
            vec_idx[i] = d.pos2idx(vec_pos[i])
        return vec_idx

    def from_vec_pos_to_vec_label(self, vec_pos):
        """
        :param vec_pos:  [0,3,4]
        :return: ['dimension 1 label or index', 'dimension 2 label  or index', 'dimension 3 label  or index']
        """
        vec_idx = len(vec_pos) * [None]
        for i in range(len(vec_pos)):
            dname = self.__dim_ids[i]
            d = self.__id2pos[dname]

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
        return [self.__id2pos[iid].pos() for iid in lst_ids]

    #
    # generator
    #

    def all_pos(self, blocked_dims={}, order=None):
        """

        :param blocked_dims:  {"year":2013, country:"IT"}
        :param order
        :return:
        """

        ids = self.__dim_ids

        vec_pos_blocked = len(ids) * [False]
        vec_pos = len(ids) * [0]  # [0,0,0]

        for (cat,idx) in blocked_dims.items():
            d = self.dimension(cat)
            vec_pos_blocked[d.pos()] = True
            vec_pos[d.pos()] = d.idx2pos(idx)

        dsizes = self.__dim_sizes
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

    def generate_all_vec(self, **blocked_dims):
        for vec_pos in self.all_pos(blocked_dims):
            vec_idx = self.from_vec_pos_to_vec_idx(vec_pos)
            value = self.value_from_vec_pos(vec_pos)

    #
    # transforming function
    #

    def to_table(self, content="label", order=None, rtype=list, blocked_dims={}):
        """
        Transforms a dataset into a table (a list of row)
        table len is the size of dataset + 1 for headers
        :param content can be "label" or "id"
        :param order
        :param rtype
        :param blocked_dims
        :return a list of row, first line is the header
        """
        table = []

        # header
        header = []
        if content == "label":
            for dname in self.__dim_ids:
                header.append(self.__id2pos[dname].label())
        else:
            header = list(self.__dim_ids)

        header.append("Value")

        # data
        table.append(header)
        for vec_pos in self.all_pos(order=order,blocked_dims=blocked_dims):
            value = self.value_from_vec_pos(vec_pos)
            if content == "label":
                row = self.from_vec_pos_to_vec_label(vec_pos)
            else:
                row = self.from_vec_pos_to_vec_idx(vec_pos)
            row.append(value)
            table.append(row)

        if rtype == pd.DataFrame:
            ret = pd.DataFrame(table[1:],columns=table[0])
        else:
            ret = table

        return ret

    def to_data_frame(self, index, content="label", order=None, blocked_dims={}):
        """
        Transform dataset to pandas data frame
              col ->
         row

        extract_bidimensional("year", "country")
        generate the following dataframe:
        year  |  country
        2010  |  1
        2011  |  2
        2012  |  3

        :param index:
        :param blocked_dims:
        :return:
        """

        # index_pos = self.__id2pos[index].pos()
        # columns = []
        # for (cat,idx) in blocked_dims.items():
        #     columns.append(idx)
        # indexes = []
        # values = []
        # for vec_pos in self.all_pos(blocked_dims):
        #     vec_idx = self.from_vec_pos_to_vec_idx(vec_pos)
        #     value = self.value_from_vec_pos(vec_pos)
        #     indexes.append(vec_idx[index_pos])
        #     values.append(value)
        #
        # df = pd.DataFrame(values,
        #                   columns=columns,
        #                   index=indexes)
        df = self.to_table(content=content, order=order, rtype=pd.DataFrame, blocked_dims=blocked_dims)
        df.index = df[index]
        del df[index]
        return df

    #
    # Parsing code
    #

    def from_file(self, filename):
        """
        read a jsonstat from a file and parse it to initialize this (empty) dataset
        :param filename: path of the file.
        :return itself to chain call
        """
        with open(filename) as f:
            json_string = f.read()
            self.from_string(json_string)
        return self

    def from_string(self, json_string):
        """
        parse a string to initialize this (empty) dataset
        :param json_string:
        :return itself to chain call
        """

        json_data = json.loads(json_string)
        self.from_json(json_data)
        return self

    def from_json(self, json_data, version=1):
        """
        parse a json structure to initialize this (empty) dataset
        :param json_data:
        :param version:
        :return itself to chain call
        """
        if version == 2:
            self.from_json_v2(json_data)
        else:
            self.from_json_v1(json_data)
        return self

    # TODO: this is meant of internal function of jsonstat not public api
    def from_json_v1(self, json_data):
        """
        parse a json structure in accordance (?) to jsonstat format version 1.x
        :param json_data: json structure
        """

        if 'label' in json_data:
            self.__label = json_data['label']
            if self.__name is None:
                self.__name = self.__label

        if 'source' in json_data:
            self.__source = json_data['source']

        if 'title' in json_data:
            self.__title = json_data['title']

        # values
        if 'value' not in json_data:
            msg = "dataset '{}': missing 'value' key".format(self.__name)
            raise JsonStatMalformedJson(msg)

        self.__value = json_data['value']
        if len(self.__value) == 0:
            msg = "dataset '{}': field 'value' is empty".format(self.__name)
            raise JsonStatMalformedJson(msg)

        if 'dimension' not in json_data:
            msg = "dataset '{}': missing 'dimension' key".format(self.__name)
            raise JsonStatMalformedJson(msg)

        # parsing dimension
        json_data_dimension = json_data['dimension']
        if 'id' not in json_data_dimension:
            msg = "dataset '{}': missing 'dimension.id' key".format(self.__name)
            raise JsonStatMalformedJson(msg)

        if 'size' not in json_data_dimension:
            msg = "dataset '{}': missing 'dimension.size' key".format(self.__name)
            raise JsonStatMalformedJson(msg)

        self.__parse_dimensions(json_data_dimension)

        # validate
        size_total = reduce(lambda x, y: x * y, self.__dim_sizes)
        if len(self.__value) != size_total:
            msg = "dataset '{}': size {} is different from calculate size {} by dimension"
            msg = msg.format(self.__name, len(self.__value), size_total)
            raise JsonStatMalformedJson(msg)

        # acc_vector
        acc = 1
        self.__acc_vector = self.__dim_nr * [1]
        i = self.__dim_nr - 2
        while i >= 0:
            acc = acc * self.__dim_sizes[i + 1]
            self.__acc_vector[i] = acc
            i -= 1

        self.__valid = True

    def __parse_dimensions(self, json_data_dimension):

        self.__dim_ids = json_data_dimension['id']
        self.__dim_sizes = json_data_dimension['size']
        self.__dim_nr = len(self.__dim_ids)

        if len(self.__dim_ids) != len(self.__dim_sizes):
            msg = "dataset '{}': dataset_id is different of dataset_size".format(self.__name)
            raise JsonStatMalformedJson(msg)

        # parsing roles
        roles = {}
        if 'role' in json_data_dimension:
            json_roles = json_data_dimension['role']
            for r in json_roles.items():
                role = r[0]
                for dname in r[1]:
                    roles[dname] = role

        # parsing each dimensions
        self.__pos2dim = len(self.__dim_ids) * [None]
        for dpos in range(len(self.__dim_ids)):
            dname = self.__dim_ids[dpos]
            dsize = self.__dim_sizes[dpos]

            if dname not in json_data_dimension:
                msg = "dataset '{}': malformed json: missing key {} in dimension".format(self.__name, dname)
                raise JsonStatException(msg)

            dimension = JsonStatDimension(dname, dsize, dpos, roles.get(dname))
            dimension.from_json(json_data_dimension[dname])
            self.__id2pos[dname] = dimension
            self.__pos2dim[dpos] = dimension

    # TODO: this is meant of internal function of jsonstat not public api
    def from_json_v2(self, json_data):
        """
        parse a jsonstat structure complaint to jsonstat format version 2.x
        :param json_data: json structure
        """

        #
        # list of keys to be parsed
        # version
        # class
        # id
        # size
        # role
        # value
        # status
        # dimension
        # link
        # {
        #	"class" : "dataset",
        #	"href" : "http://json-stat.org/samples/oecd.json",
        #	"label" : "Unemployment rate in the OECD countries 2003-2014"
        # }

        if "href" in json_data:
            self.__href = json_data["href"]

        if 'label' in json_data:
            self.__label = json_data['label']
            if self.__name is None:
                self.__name = self.__label

        if "id" not in json_data:
            if "href" in json_data:
                # todo skip the next section???
                # todo: download data?
                return

        # parsing when values are presents
        self.__dim_ids = json_data['id']
        self.__dim_sizes = json_data['size']
        self.__dim_nr = len(self.__dim_ids)

        # validate len(ids) == len(sizes)
        if len(self.__dim_ids) != len(self.__dim_sizes):
            msg = "dataset '{}': dataset_id is different of dataset_size".format(self.__name)
            raise JsonStatMalformedJson(msg)

        # parsing roles
        roles = {}
        if 'role' in json_data:
            json_roles = json_data['role']
            for r in json_roles.items():
                role = r[0]
                for dname in r[1]:
                    roles[dname] = role

        # value is required
        # https://json-stat.org/format/#value
        # TODO: value into a numpy array?
        self.__value = json_data['value']
        if len(self.__value) == 0:
            msg = "dataset '{}': field 'value' is empty".format(self.__name)
            raise JsonStatMalformedJson(msg)

            # TODO: parsing status
            # dimension

            # TODO: parsing link
