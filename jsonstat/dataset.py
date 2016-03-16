# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
from functools import reduce
from collections import namedtuple
import json

# packages
import numpy as np
import pandas as pd

# jsonstat
from jsonstat.dimension import JsonStatDimension
from jsonstat.exceptions import JsonStatException
from jsonstat.exceptions import JsonStatMalformedJson

JsonStatValue = namedtuple('JsonStatValue', ['value', 'status'])


class JsonStatDataSet:
    """Represents a JsonStat dataset"""

    def __init__(self, dataset_name=None):
        """Initialize an empty dataset.

        Dataset could have a name if we parse a jsonstat format version 1.
        :param dataset_name: dataset name (jsonstat v.1)
        """
        self.__valid = False
        self.__json_data = None

        self.__name = dataset_name
        self.__title = None
        self.__label = None
        self.__source = None

        # dimensions
        self.__dim_nr = 0
        self.__pos2iid = None
        self.__dimension_sizes = None

        self.__pos2dim = []   # array int -> dim
        self.__pos2size = []  # array int -> int (dimension size)
        self.__iid2dim = {}   # dict  id  -> pos
        self.__lbl2dim = {}   # dict  lbl -> dim
        self.__lbl2pos = {}   # dict  lbl -> pos

        self.__value = None
        self.__status = None

    def name(self):
        """Returns the name of the dataset"""
        return self.__name

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
        """used by ipython to make a better representation"""
        return self.__str__()

    def info(self):
        """print some info about this dataset on stdout"""
        print(self)

    #
    # dimensions
    #

    def __len__(self):
        """returns the size of the dataset"""
        return len(self.__value)

    def dimensions(self):
        """returns list of JsonStatDimension"""
        return self.__pos2dim

    def dimension(self, spec):
        """get a dimension by spec

        :param spec: name (string) or id of the dimension
        :returns: a JsonStatDimension
        """
        if type(spec) is int:
            return self.__pos2dim[spec]
        if spec not in self.__iid2dim:
            msg = "dataset '{}': unknown dimension '{}' know dimensions ids are: {}".format(self.__name, spec, ", ".join(self.__pos2iid))
            raise JsonStatException(msg)
        return self.__iid2dim[spec]

    def __str__dimensions(self):
        out = "{} dimensions:\n".format(len(self.__pos2iid))
        for i, dname in enumerate(self.__pos2iid):
            d = self.__iid2dim[dname]
            out += "  {}: dim id: '{}' label: '{}' size: '{}' role: '{}'\n".format(i, d.name(), d.label(), len(d), d.role())
        return out

    def info_dimensions(self):
        """print same info on dimensions on stdout"""
        print(self.__str__dimensions())

    #
    # value/status
    #

    def data(self, *args, **kargs):
        if not self.__valid:
            raise JsonStatException('dataset not initialized')

        #
        # value
        #
        if len(args) == 1:
            dims = args[0]
        else:
            dims = kargs
        apos = self._from_adim_to_apos(dims)
        idx = self._from_apos_to_idx(apos)
        value = self.__value[idx]

        #
        # status
        #
        if self.__status is None:
            status = None
        elif isinstance(self.__status, str):
            status = self.__status
        elif isinstance(self.__status, list) and len(self.__status) == 1:
            status = self.__status[0]
        elif isinstance(self.__status, dict) and idx not in self.__status:
            status = None
        else:
            status = self.__status[idx]
        return JsonStatValue(value, status)

    def value(self, *args, **kargs):
        """get a value

        :param kargs: { cat1:value1, ..., cati:valuei, ... }
            cati can be the id of the dimension or the label of dimension
            valuei can be the index or label of category
            ex.:{country:"AU", "year":"2014"}

        :returns: value (typically a number)
        """
        if not self.__valid:
            raise JsonStatException('dataset not initialized')

        if len(args) == 1:
            dims = args[0]
        else:
            dims = kargs
        apos = self._from_adim_to_apos(dims)
        idx = self._from_apos_to_idx(apos)
        value = self.__value[idx]
        return value

    def status(self, *args, **kargs):
        """get a status

        :param kargs: { cat1:value1, ..., cati:valuei, ... }
            cati can be the id of the dimension or the label of dimension
            valuei can be the index or label of category
            ex.:{country:"AU", "year":"2014"}

        :returns: value (typically a number)
        """
        if not self.__valid:
            raise JsonStatException('dataset not initialized')

        if self.__status is None:
            status = None
        elif isinstance(self.__status, str):
            status = self.__status
        elif isinstance(self.__status, list) and len(self.__status) == 1:
            status = self.__status[0]
        else:
            if len(args) == 1:
                dims = args[0]
            else:
                dims = kargs
            apos = self._from_adim_to_apos(dims)
            idx = self._from_apos_to_idx(apos)

            if isinstance(self.__status, dict) and idx not in self.__status:
                status = None
            else:
                status = self.__status[idx]
        return status

    def __value_from_vec_pos(self, lst):
        """

        :param lst: [0,3,4]
        :returns: value at dimension [0,3,4]
        """
        return self.__value[self._from_apos_to_idx(lst)]

    #
    # transform function about dimensions indexes
    # this functions are only for library internal usage

    # def _from_vec_dimid_to_vec_pos(self, dims):
    #     """Transforms a dimension dict to dimension array
    #
    #         key can be only ID
    #         {"country":"AU", "year":2014} -> [1,2,3]
    #     :param dims: {country:"AU", "year":2014}
    #     :returns: [1,2,3]
    #     """
    #     vec_pos = len(self.__pos2iid) * [0]
    #     for (cat, val) in dims.items():
    #         if cat not in self.__iid2dim:
    #             allowed_categories = ", ".join(self.__pos2iid)
    #             msg = "dataset '{}': category '{}' don't exists allowed category are: {}"
    #             msg = msg.format(self.__name, cat, allowed_categories)
    #             raise JsonStatException(msg)
    #         dim = self.__iid2dim[cat]
    #         vec_pos[dim.pos()] = dim.idx2pos(val)
    #     return vec_pos

    def _from_adim_to_apos(self, dims):
        """Transforms a dimension dict to dimension array

            {"country":"AU", "year":2014} -> [1,2,3]
        :param dims: keys are dimension (id or label), value are categories
             "country" is the id of dimension
             "AU" is the category of dimension
        :returns: a list of integer
        """
        apos = len(self.__pos2iid) * [0]
        for (cat, val) in dims.items():
            # key is id
            if cat in self.__iid2dim:
                dim = self.__iid2dim[cat]
            # key is label
            elif cat in self.__lbl2pos:
                dim = self.__lbl2dim[cat]
            # key is not id or label so raise error
            else:
                allowed_categories = ", ".join(self.__pos2iid)
                msg = "dataset '{}': category '{}' don't exists allowed category are: {}"
                msg = msg.format(self.__name, cat, allowed_categories)
                raise JsonStatException(msg)

            apos[dim.pos()] = dim.idx_or_lbl_2pos(val)
        return apos

    def _from_apos_to_idx(self, lst):
        """from a list of position get a index into value array

        [1,2,3] -> 10
        :param lst: list of integer
        :returns: an integer index into values
        """
        s = np.array(self.__acc_vector)
        r = s * lst
        return np.sum(r)

    def _from_apos_to_aidx(self, vec_pos, without_one_dimension=False):
        """transforms an array of pos into ana arry of idc

        [0,3,4] -> ['dimension 1 index', 'dimension 2 label', 'dimension 3 label']

        :param vec_pos:  [0,3,4]
        :returns: ['dimension 1 index', 'dimension 2 label', 'dimension 3 label']
        """
        # vec_idx = len(vec_pos) * [None]
        vec_idx = []
        for pos in range(len(vec_pos)):
            dim_iid = self.__pos2iid[pos]
            dim = self.__iid2dim[dim_iid]
            # vec_idx[i] = dim.pos2idx(vec_pos[i])
            if not(without_one_dimension and len(dim) == 1):
                vec_idx.append(dim.pos2idx(vec_pos[pos]))
        return vec_idx

    def _from_apos_to_alabel(self, vec_pos, without_one_dimension=False):
        """transforms on array of dim into an array of label

        :param vec_pos:  [0,3,4]
        :returns: ['dimension 1 label or index', 'dimension 2 label  or index', 'dimension 3 label  or index']
        """

        # vec_idx = len(vec_pos) * [None]
        vec_idx = []
        for pos in range(len(vec_pos)):
            dim_iid = self.__pos2iid[pos]
            dim = self.__iid2dim[dim_iid]

            lbl = dim.pos2label(vec_pos[pos])
            if lbl is None:
                lbl = dim.pos2idx(vec_pos[pos])

            # vec_idx[i] = lbl
            if not(without_one_dimension and len(dim) == 1):
                vec_idx.append(lbl)

        return vec_idx

    def _from_aidx_to_adim(self, lst_iids):
        """From a list of dimension name to a list of numerical dimension position

          F.e.
          ["year", "country"] -> [1,0]
          ["country", "year"] -> [0,1]

        :returns: list of number
        """
        return [self.__iid2dim[iid].pos() for iid in lst_iids]

    #
    # generators
    #

    def all_pos(self, blocked_dims={}, order=None):
        """all_pos doc

        :param blocked_dims:  {"year":2013, country:"IT"}
        :param order: order
        :returns:
        """

        nrdim = len(self.__pos2iid)
        if order is not None and len(order) != nrdim:
            msg = "length of the order vector is different from number of dimension {}".format(nrdim)
            raise JsonStatException(msg)

        vec_pos_blocked = nrdim * [False]
        vec_pos = nrdim * [0]

        for (cat,idx) in blocked_dims.items():
            d = self.dimension(cat)
            vec_pos_blocked[d.pos()] = True
            vec_pos[d.pos()] = d.idx2pos(idx)

        pos2size = self.__pos2size

        if order is None:
            vec_dimension_reorder = range(nrdim)
        else:
            vec_dimension_reorder = order

        nrd = nrdim - 1
        while nrd >= 0:

            yield list(vec_pos)  # make a shallow copy of vec_pos

            nrd = nrdim - 1
            cur_dim = vec_dimension_reorder[nrd]
            # se la posizione non e bloccata allora puoi far andare avanti la cifra
            if not vec_pos_blocked[cur_dim]:
                vec_pos[cur_dim] += 1

            # se non si arrivati all'ultima dimensione
            # e se la dimensione corrente non e al massimo valore o se la dimensione corrente e bloccata
            while nrd >= 0 and \
                    (vec_pos[cur_dim] == pos2size[cur_dim] or vec_pos_blocked[cur_dim]):

                # se la posizione non e' bloccata allora puoi far partire il valore dall'inizio
                if not vec_pos_blocked[cur_dim]:
                    vec_pos[cur_dim] = 0

                # esamina la prossima posizione
                nrd -= 1
                # se la dimensione corrente non e' la prima
                if nrd >= 0:
                    cur_dim = vec_dimension_reorder[nrd]
                    # se la dimensione corrente non e bloccata puoi farla avanzare
                    if not vec_pos_blocked[cur_dim]:
                        vec_pos[cur_dim] += 1

    def generate_all_vec(self, **blocked_dims):
        for vec_pos in self.all_pos(blocked_dims):
            vec_idx = self._from_apos_to_aidx(vec_pos)
            value = self.__value_from_vec_pos(vec_pos)

    #
    # transforming function
    #

    def to_table(self, content="label", order=None, rtype=list, blocked_dims={}, value_column="Value",
                 without_one_dimensions=False):
        """Transforms a dataset into a table (a list of row)

        table len is the size of dataset + 1 for headers

        :param content: can be "label" or "id"
        :param order:
        :param rtype:
        :param blocked_dims:
        :returns: a list of row, first line is the header
        """
        table = []

        # header
        header = []
        if content == "label":
            for dname in self.__pos2iid:
                header.append(self.__iid2dim[dname].label())
        else:
            header = list(self.__pos2iid)

        header.append(value_column)

        # data
        table.append(header)
        for vec_pos in self.all_pos(order=order,blocked_dims=blocked_dims):
            value = self.__value_from_vec_pos(vec_pos)
            if content == "label":
                row = self._from_apos_to_alabel(vec_pos, without_one_dimension=without_one_dimensions)
            else:
                row = self._from_apos_to_aidx(vec_pos, without_one_dimension=without_one_dimensions)
            row.append(value)
            table.append(row)

        if rtype == pd.DataFrame:
            ret = pd.DataFrame(table[1:],columns=table[0])
        else:
            ret = table

        return ret

    def to_data_frame(self, index, content="label", order=None, blocked_dims={},value_column="Value"):
        """Transform dataset to pandas data frame

        extract_bidimensional("year", "country")
        generate the following dataframe:
        year  |  country
        2010  |  1
        2011  |  2
        2012  |  3

        :param index:
        :param content:
        :param blocked_dims:
        :param order:
        :param value_column:

        :returns:
        """

        df = self.to_table(content=content, order=order, rtype=pd.DataFrame,
                           blocked_dims=blocked_dims, value_column=value_column)
        # TODO: avoid creating a new dataframe (?)
        # df.index = df[index]
        # del df[index]
        df = df.set_index([index])
        return df

    #
    # Parsing code
    #

    def from_file(self, filename):
        """read a jsonstat from a file and parse it to initialize this (empty) dataset

        :param filename: path of the file.
        :returns: itself to chain call
        """
        with open(filename) as f:
            json_string = f.read()
            self.from_string(json_string)
        return self

    def from_string(self, json_string):
        """parse a string to initialize this (empty) dataset

        :param json_string:
        :returns: itself to chain call
        """
        # TODO: try to determinate the json-stat version
        json_data = json.loads(json_string)
        self.from_json(json_data)
        return self

    def from_json(self, json_data, version=1):
        """parse a json structure to initialize this (empty) dataset

        :param json_data: json structure
        :param version: json stat version
        :returns: itself to chain call
        """
        if version == 2:
            self._from_json_v2(json_data)
        else:
            self._from_json_v1(json_data)
        return self

    # TODO: this is meant to be an internal function of jsonstat it is not public api
    def _from_json_v1(self, json_data):
        """parse a json structure in accordance (?) to jsonstat format version 1.x

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

        # parsing value
        if 'value' not in json_data:
            msg = "dataset '{}': missing 'value' key".format(self.__name)
            raise JsonStatMalformedJson(msg)
        self.__value = json_data['value']

        if len(self.__value) == 0:
            msg = "dataset '{}': field 'value' is empty".format(self.__name)
            raise JsonStatMalformedJson(msg)

        # https://json-stat.org/format/#status
        # parsing status
        #
        # eurostat has the following structure for status
        # status : {
        #   'value' : { "": "" }
        #   'category' : { ... }
        # }

        if 'status' in json_data:
            self.__status = json_data['status']
            if isinstance(self.__status, list):
                if len(self.__status) != 1 and len(self.__status) != len(self.__value):
                    msg = "dataset '{}': incorrect size of status fields"
                    raise JsonStatMalformedJson(msg)
            if isinstance(self.__status, dict):
                # convert key into int
                # eurostat data has incorrect status { "":"" }
                nd = {}
                for k, v in self.__status.items():
                    try:
                        nd[int(k)] = v
                    except ValueError:
                        pass
                self.__status = nd

        #
        # parsing dimension
        #
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

        self.__pos2iid = json_data_dimension['id']
        self.__pos2size = json_data_dimension['size']
        self.__dim_nr = len(self.__pos2iid)

        # validate dimension
        if len(self.__pos2iid) != len(self.__pos2size):
            msg = "dataset '{}': dataset_id is different of dataset_size".format(self.__name)
            raise JsonStatMalformedJson(msg)

        json_data_roles = None
        if 'role' in json_data_dimension:
            json_data_roles = json_data_dimension['role']
        self.__parse_dimensions(json_data_dimension, json_data_roles)

        # validate
        size_total = reduce(lambda x, y: x * y, self.__pos2size)
        if len(self.__value) != size_total:
            msg = "dataset '{}': size {} is different from calculate size {} by dimension"
            msg = msg.format(self.__name, len(self.__value), size_total)
            raise JsonStatMalformedJson(msg)

        self.__compute_acc_vector()
        self.__valid = True

    # TODO: this is meant to be an internal function of jsonstat it is not public api
    def _from_json_v2(self, json_data):
        """parse a jsonstat structure complaint to jsonstat format version 2.x

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

        # value is required
        # https://json-stat.org/format/#value
        # TODO: value into a numpy array?
        self.__value = json_data['value']
        if len(self.__value) == 0:
            msg = "dataset '{}': field 'value' is empty".format(self.__name)
            raise JsonStatMalformedJson(msg)

        # parsing when values are presents
        self.__pos2iid = json_data['id']
        self.__pos2size = json_data['size']
        self.__dim_nr = len(self.__pos2iid)

        # validate len(ids) == len(sizes)
        if len(self.__pos2iid) != len(self.__pos2size):
            msg = "dataset '{}': dataset_id is different of dataset_size".format(self.__name)
            raise JsonStatMalformedJson(msg)

        # https://json-stat.org/format/#status
        # parsing status
        if 'status' in json_data:
            self.__status = json_data['status']
            if isinstance(self.__status, list):
                if len(self.__status) != 1 and len(self.__status) != len(self.__value):
                    msg = "dataset '{}': incorrect size of status fields"
                    raise JsonStatMalformedJson(msg)
            if isinstance(self.__status, dict):
                # convert key into int
                self.__status = {int(k): v for k, v in self.__status.items()}

        # dimension
        json_data_roles = None
        if 'role' in json_data:
            json_data_roles = json_data['role']
        json_data_dimension = json_data["dimension"]
        self.__parse_dimensions(json_data_dimension, json_data_roles)

        # TODO: parsing link

        self.__compute_acc_vector()
        self.__valid = True

    def __parse_dimensions(self, json_data_dimension, json_data_roles):
        """Parse dimension in json stat

        it used for format v1 and v2

        :param json_data_dimension:
        :param json_data_roles:
        :returns:
        """

        # parsing roles
        roles = {}
        if json_data_roles is not None:
            json_roles = json_data_roles
            for r in json_roles.items():
                role = r[0]
                for dname in r[1]:
                    roles[dname] = role

        # parsing each dimensions
        self.__pos2dim = len(self.__pos2iid) * [None]
        for dpos in range(len(self.__pos2iid)):
            dname = self.__pos2iid[dpos]
            dsize = self.__pos2size[dpos]

            if dname not in json_data_dimension:
                msg = "dataset '{}': malformed json: missing key {} in dimension".format(self.__name, dname)
                raise JsonStatException(msg)

            dimension = JsonStatDimension(dname, dsize, dpos, roles.get(dname))
            dimension.from_json(json_data_dimension[dname])
            self.__iid2dim[dname] = dimension
            self.__pos2dim[dpos] = dimension
            if dimension.label() is not None:
                self.__lbl2dim[dimension.label()] = dimension
                self.__lbl2pos[dimension.label()] = dpos

    def __compute_acc_vector(self):
        acc = 1
        self.__acc_vector = self.__dim_nr * [1]
        i = self.__dim_nr - 2
        while i >= 0:
            acc = acc * self.__pos2size[i + 1]
            self.__acc_vector[i] = acc
            i -= 1
