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
import terminaltables

# jsonstat
from jsonstat.value import JsonStatValue
from jsonstat.dimension import JsonStatDimension
from jsonstat.exceptions import JsonStatException
from jsonstat.exceptions import JsonStatMalformedJson
from jsonstat.utility import lst2html


class JsonStatDataSet:
    """Represents a JsonStat dataset

        >>> import os, jsonstat  # doctest: +ELLIPSIS
        >>> filename = os.path.join(jsonstat.__fixtures_dir, "www.json-stat.org", "oecd-canada-col.json")
        >>> dataset = jsonstat.from_file(filename).dataset(0)
        >>> dataset.label
        'Unemployment rate in the OECD countries 2003-2014'
        >>> print(dataset)
        name:   'Unemployment rate in the OECD countries 2003-2014'
        label:  'Unemployment rate in the OECD countries 2003-2014'
        size: 432
        +-----+---------+--------------------------------+------+--------+
        | pos | id      | label                          | size | role   |
        +-----+---------+--------------------------------+------+--------+
        | 0   | concept | indicator                      | 1    | metric |
        | 1   | area    | OECD countries, EU15 and total | 36   | geo    |
        | 2   | year    | 2003-2014                      | 12   | time   |
        +-----+---------+--------------------------------+------+--------+
        >>> dataset.dimension(1)
        +-----+--------+----------------------------+
        | pos | idx    | label                      |
        +-----+--------+----------------------------+
        | 0   | 'AU'   | 'Australia'                |
        | 1   | 'AT'   | 'Austria'                  |
        | 2   | 'BE'   | 'Belgium'                  |
        | 3   | 'CA'   | 'Canada'                   |
        | 4   | 'CL'   | 'Chile'                    |
        | 5   | 'CZ'   | 'Czech Republic'           |
        | 6   | 'DK'   | 'Denmark'                  |
        | 7   | 'EE'   | 'Estonia'                  |
        | 8   | 'FI'   | 'Finland'                  |
        | 9   | 'FR'   | 'France'                   |
        | 10  | 'DE'   | 'Germany'                  |
        | 11  | 'GR'   | 'Greece'                   |
        | 12  | 'HU'   | 'Hungary'                  |
        | 13  | 'IS'   | 'Iceland'                  |
        | 14  | 'IE'   | 'Ireland'                  |
        | 15  | 'IL'   | 'Israel'                   |
        | 16  | 'IT'   | 'Italy'                    |
        | 17  | 'JP'   | 'Japan'                    |
        | 18  | 'KR'   | 'Korea'                    |
        | 19  | 'LU'   | 'Luxembourg'               |
        | 20  | 'MX'   | 'Mexico'                   |
        | 21  | 'NL'   | 'Netherlands'              |
        | 22  | 'NZ'   | 'New Zealand'              |
        | 23  | 'NO'   | 'Norway'                   |
        | 24  | 'PL'   | 'Poland'                   |
        | 25  | 'PT'   | 'Portugal'                 |
        | 26  | 'SK'   | 'Slovak Republic'          |
        | 27  | 'SI'   | 'Slovenia'                 |
        | 28  | 'ES'   | 'Spain'                    |
        | 29  | 'SE'   | 'Sweden'                   |
        | 30  | 'CH'   | 'Switzerland'              |
        | 31  | 'TR'   | 'Turkey'                   |
        | 32  | 'UK'   | 'United Kingdom'           |
        | 33  | 'US'   | 'United States'            |
        | 34  | 'EU15' | 'Euro area (15 countries)' |
        | 35  | 'OECD' | 'total'                    |
        +-----+--------+----------------------------+
        >>> dataset.data(0)
        JsonStatValue(idx=0, value=5.943826289, status=None)
    """

    def __init__(self, name=None):
        """Initialize an empty dataset.

        Dataset could have a name (key) if we parse a jsonstat format version 1.

        :param name: dataset name (for jsonstat v.1)
        """
        self.__valid = False

        self.__name = name
        self.__title = None
        self.__label = None
        self.__source = None

        # dimensions
        self.__dim_nr = 0  # len(self.__pos2dim)

        self.__pos2size = []  # array int -> int (dimension size)
        self.__pos2mult = None  # array int -> multiplicative factor

        self.__pos2dim = []  # array int -> dim
        self.__did2dim = {}  # dict  id  -> dim
        self.__lbl2dim = {}  # dict  lbl -> dim

        self.__value = None
        self.__status = None

    @property
    def name(self):
        """
        :getter: returns the name of the dataset
        :type: string
        """
        return self.__name

    @property
    def label(self):
        """
        :getter: returns the label of the dataset
        :type: string
        """
        return self.__label

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

    def _repr_html_(self):
        """used by ipython to make a better representation"""

        html = ""
        if self.__name is not None:
            html += "name:   '{}'</br>".format(self.__name)

        if self.__title is not None:
            html += "title:  '{}'</br>".format(self.__title)

        if self.__label is not None:
            html += "label:  '{}'</br>".format(self.__label)

        if self.__source is not None:
            html += "source: '{}'</br>".format(self.__label, self.__source)

        html += "size: {}</br>".format(len(self))
        lst = self.__dim_to_table()
        html += lst2html(lst)
        return html

    def __len__(self):
        """returns the size of the dataset"""
        return len(self.__value)

    #
    # dimensions
    #

    def dimensions(self):
        """returns list of JsonStatDimension"""
        return self.__pos2dim

    def dimension(self, spec):
        """get a JsonStatDimension by spec

        :param spec: spec can be:
         - (string) or id of the dimension
         - int position of dimension
        :returns: a JsonStatDimension
        """
        if type(spec) is int:
            return self.__pos2dim[spec]
        if spec not in self.__did2dim:
            msg = "dataset '{}': unknown dimension '{}' know dimensions ids are: {}"
            msg = msg.format(self.__name, spec, ", ".join([dim.did for dim in self.__pos2dim]))
            raise JsonStatException(msg)
        return self.__did2dim[spec]

    def __dim_to_table(self):
        lst = [["pos", "id", "label", "size", "role"]]
        for i, dim in enumerate(self.__pos2dim):
            row = [str(i), dim.did, dim.label, str(len(dim)), dim.role]
            row = list(map(lambda x: "" if x is None else x, row))
            lst.append(row)
        return lst

    def __str__dimensions(self):
        lst = self.__dim_to_table()

        table = terminaltables.AsciiTable(lst)
        # table.justify_columns = {2: "right", 4: "right"}
        out = table.table
        return out

    def info_dimensions(self):
        """print same info on dimensions on stdout"""
        print(self.__str__dimensions())

    #
    # querying value/status
    #

    def data(self, *args, **kargs):
        """Returns a JsonStatValue containings value and status about a datapoint
        The datapoint will be retrieved according the parameters

        :param args:
            - data(<int>)  where i is index into the
            - data(<list>) where lst = [i1,i2,i3,...]) each i indicate the dimension len(lst) == number of dimension
            - data(<dict>) where dict is {k1:v1, k2:v2, ...} dimension of size 1 can be ommitted

        :param kargs:
            - data(k1=v1,k2=v2,...) where **ki** are the id or label of dimension
              **vi** are the index or label of the category dimension of size 1 can be ommitted

        :returns: a JsonStatValue object

        kargs { cat1:value1, ..., cati:valuei, ... }
        cati can be the id of the dimension or the label of dimension
        valuei can be the index or label of category
        ex.:{country:"AU", "year":"2014"}

        >>> import os, jsonstat  # doctest: +ELLIPSIS
        >>> filename = os.path.join(jsonstat.__fixtures_dir, "www.json-stat.org", "oecd-canada-col.json")
        >>> dataset = jsonstat.from_file(filename).dataset(0)
        >>> dataset.data(0)
        JsonStatValue(idx=0, value=5.943826289, status=None)
        >>> dataset.data(concept='UNR', area='AU', year='2003')
        JsonStatValue(idx=0, value=5.943826289, status=None)
        >>> dataset.data(area='AU', year='2003')
        JsonStatValue(idx=0, value=5.943826289, status=None)
        >>> dataset.data({'area':'AU', 'year':'2003'})
        JsonStatValue(idx=0, value=5.943826289, status=None)
        """
        if not self.__valid:
            raise JsonStatException('dataset not initialized')

        # decoding args
        idx = self._2idx(*args, **kargs)
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
        return JsonStatValue(idx, value, status)

    def value(self, *args, **kargs):
        """get a value
        For the parameters see py:meth:`jsonstat.JsonStatDataSet.data`.

        :returns: value (typically a number)
        """
        # TODO: add onlyvalue=true to extract only the value
        return self.data(*args, **kargs).value

    def status(self, *args, **kargs):
        """get datapoint status

        For the parameters see py:meth:`jsonstat.JsonStatDataSet.data`.

        :returns: status (typically a string)
        """
        # TODO: add onlystatus=true to extract only the value?
        return self.data(*args, **kargs).status

    def __value_from_vec_pos(self, lst):
        """

        :param lst: [0,3,4]
        :returns: value at dimension [0,3,4]
        """
        return self.__value[self.lint_as_idx(lst)]

    #
    # dataset can be access using different type of indexes
    # simple index is integer.
    # ex. dataset.data(0)
    # other type of idexes
    # lint [ <int1>, <int2>, <int3> ...]
    # lcat [ <cat1>, <cat2>, ... ]
    # dcat [ <did1>:<cat1>, <did2>:<cat1>, ... ]

    # this functions are only for library internal usage
    #

    def _2idx(self, *args, **kargs):
        """convert args to integer index """

        if len(args) == 1:
            # data(int)
            if isinstance(args[0], int):
                return args[0]
            # data([i1,i2,i3])
            elif isinstance(args[0], list):
                idx = self.lint_as_idx(args[0])
                return idx
            # data({k1:v1, k2:v2})
            elif isinstance(args[0], dict):
                dims = args[0]
                apos = self.dcat_to_lint(dims)
                idx = self.lint_as_idx(apos)
                return idx
        elif len(args) == 0:
            # data(k1:v1, k2:v2)
            dims = kargs
            # print(dims)
            apos = self.dcat_to_lint(dims)
            # print(apos)
            idx = self.lint_as_idx(apos)
            # print(idx)
            return idx

        msg = "unexpected parameters"
        raise JsonStatException(msg)

    def dcat_to_lint(self, dims):
        """Transforms a dimension dict to dimension array

        ::

            {"country":"AU", "year":2014} -> [1,2,3]

        :param dims: keys are dimension (id or label), value are categories
             "country" is the id of dimension
             "AU" is the category of dimension
        :returns: a list of integer
        """
        apos = len(self.__pos2dim) * [0]
        for (cat, val) in dims.items():
            # key is id
            if cat in self.__did2dim:
                dim = self.__did2dim[cat]
            # key is label
            elif cat in self.__lbl2dim:
                dim = self.__lbl2dim[cat]
            # key is not id or label so raise error
            else:
                allowed_categories = ", ".join(["'{}'".format(dim.did) for dim in self.__pos2dim])
                msg = "dataset '{}': category '{}' don't exists allowed categories are: {}"
                msg = msg.format(self.__name, cat, allowed_categories)
                raise JsonStatException(msg)

            apos[dim.pos] = dim.category(val).pos
        return apos

    def lint_as_idx(self, lst):
        """from a list of position get a index into value array

        [1,2,3] -> 10
        :param lst: list of integer
        :returns: an integer index into values
        """
        s = np.array(self.__pos2mult)
        r = s * lst
        return np.sum(r)

    def idx_as_lint(self, idx):
        """ 10 -> [<int1>, <int2>, ...]
        """
        lint = self.__dim_nr * [0]
        i = len(self.__pos2size) - 1
        while idx > 0 and i != 0:
            lint[i] = idx % self.__pos2size[i]
            idx -= (lint[i] * self.__pos2mult[i])
            i -= 1
        return lint

    def idx_as_lcat(self, idx):
        lint = self.idx_as_lint(idx)
        lcat = self.lint_as_lcat(lint)
        return lcat

    def lint_as_lcat(self, lint, without_one_dimension=False):
        """transforms an array of int into an array of cat

        [0,3,4] -> ['dimension 1 index', 'dimension 2 label', 'dimension 3 label']

        :param lint:  [0,3,4]
        :returns: ['dimension 1 index', 'dimension 2 label', 'dimension 3 label']
        """
        lcat = []
        for pos, lint_pos in enumerate(lint):
            dim = self.__pos2dim[pos]
            if not (without_one_dimension and len(dim) == 1):
                cat = dim._pos2cat(lint_pos).index
                lcat.append(cat)
        return lcat

    def _lint_to_llbl(self, apos, without_one_dimension=False):
        """transforms on array of dim into an array of label

        :param apos:  [0,3,4]
        :returns: ['dimension 1 label or index', 'dimension 2 label  or index', 'dimension 3 label  or index']
        """

        # vec_idx = len(vec_pos) * [None]
        aidx = []
        for pos in range(len(apos)):
            dim = self.__pos2dim[pos]
            lbl = dim._pos2cat(apos[pos]).label
            if lbl is None:
                lbl = dim._pos2cat(apos[pos]).index

            # vec_idx[i] = lbl
            if not (without_one_dimension and len(dim) == 1):
                aidx.append(lbl)

        return aidx

    def _from_aidx_to_adim(self, ldid):
        """From a list of dimension name to a list of numerical dimension position

          F.e.
          ["year", "country"] -> [1,0]
          ["country", "year"] -> [0,1]

        :returns: list of number
        """
        return [self.__did2dim[did].pos for did in ldid]

    #
    # generators
    #

    def all_pos(self, blocked_dims={}, order=None):
        """all_pos doc

        :param blocked_dims:  {"year":2013, country:"IT"}
        :param order: order
        :returns:
        """

        nr_dim = len(self.__pos2dim)
        if order is not None:
            if len(order) != nr_dim:
                msg = "length of the order vector is different from number of dimension {}".format(nr_dim)
                raise JsonStatException(msg)
            if not isinstance(order[1], int):
                order = [self.__did2dim[iid].pos for iid in order]

        vec_pos_blocked = nr_dim * [False]
        vec_pos = nr_dim * [0]

        for (cat, idx) in blocked_dims.items():
            d = self.dimension(cat)
            vec_pos_blocked[d.pos] = True
            vec_pos[d.pos] = d._idx2pos(idx)

        pos2size = self.__pos2size

        if order is None:
            vec_dimension_reorder = range(nr_dim)
        else:
            vec_dimension_reorder = order

        nrd = nr_dim - 1
        while nrd >= 0:

            yield list(vec_pos)  # make a shallow copy of vec_pos

            nrd = nr_dim - 1
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
            vec_idx = self.lint_as_lcat(vec_pos)
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
        if content == "label":
            header = [dim.label for dim in self.__pos2dim]
        else:
            header = [dim.did for dim in self.__pos2dim]

        header.append(value_column)

        # data
        table.append(header)
        for apos in self.all_pos(order=order, blocked_dims=blocked_dims):
            value = self.__value_from_vec_pos(apos)
            if content == "label":
                row = self._lint_to_llbl(apos, without_one_dimension=without_one_dimensions)
            else:
                row = self.lint_as_lcat(apos, without_one_dimension=without_one_dimensions)
            row.append(value)
            table.append(row)

        if rtype == pd.DataFrame:
            ret = pd.DataFrame(table[1:], columns=table[0])
        else:
            ret = table

        return ret

    def to_data_frame(self, index, content="label", order=None, blocked_dims={}, value_column="Value"):
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
        """read a jsonstat from a file and parse it to initialize this dataset.

        It is better to use :py:meth:`jsonstat.from_file`

        :param filename: path of the file.
        :returns: itself to chain calls
        """
        with open(filename) as f:
            json_string = f.read()
            self.from_string(json_string)
        return self

    def from_string(self, json_string):
        """parse a string containing a jsonstat and initialize this dataset

        It is better to use :py:meth:`jsonstat.from_string`

        :param json_string: string containing a jsonstat
        :returns: itself to chain calls
        """
        json_data = json.loads(json_string)
        self.from_json(json_data)
        return self

    def from_json(self, json_data):
        """parse a json structure and initialize this dataset

        It is better to use py:meth:`jsonstat.from_json`

        :param json_data: json structure
        :returns: itself to chain calls
        """
        if "version" in json_data:
            # assume version 2
            self._from_json_v2(json_data)
        else:
            self._from_json_v1(json_data)
        return self

    def _from_json_v1(self, json_data):
        """parse a json structure according to jsonstat format version 1.x

        .. warning::

            this is an internal library function (it is not public api)

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

        pos2iid = json_data_dimension['id']

        self.__pos2size = json_data_dimension['size']
        # https://github.com/26fe/jsonstat.py/issues/1
        # cso.ie expose dimension sizes as strings instead of integers.
        for i, e in enumerate(self.__pos2size):
            self.__pos2size[i] = int(e)

        self.__dim_nr = len(pos2iid)

        # validate dimension
        if len(pos2iid) != len(self.__pos2size):
            msg = "dataset '{}': dataset_id is different of dataset_size".format(self.__name)
            raise JsonStatMalformedJson(msg)

        json_data_roles = None
        if 'role' in json_data_dimension:
            json_data_roles = json_data_dimension['role']
        self.__parse_dimensions(json_data_dimension, json_data_roles, pos2iid)

        # validate
        size_total = reduce(lambda x, y: x * y, self.__pos2size)
        if len(self.__value) != size_total:
            msg = "dataset '{}': size {} is different from calculate size {} by dimension"
            msg = msg.format(self.__name, len(self.__value), size_total)
            raise JsonStatMalformedJson(msg)

        self.__compute_pos2mult()
        self.__valid = True

    def _from_json_v2(self, json_data):
        """parse a jsonstat structure compliant to jsonstat format version 2.x

        .. warning::

            this is an internal library function (it is not public api)

        :param json_data: json structure

        keys to be parsed
        - version
        - class: "dataset"

        - href: url
        - label: "..."
        - id: <list of dimension id>
        - size: <list of integer, size of dimension>
        - role: roles of dimension
        - value: <list of values>
        - status
        - dimension
        - link

        ::

            {
                "class" : "dataset",
                "href" : "http://json-stat.org/samples/oecd.json",
                "label" : "Unemployment rate in the OECD countries 2003-2014"
             }

        """

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

        pos2iid = json_data['id']

        self.__pos2size = json_data['size']
        # https://github.com/26fe/jsonstat.py/issues/1
        # cso.ie expose dimension sizes as strings instead of integers.
        for i, e in enumerate(self.__pos2size):
            self.__pos2size[i] = int(e)

        self.__dim_nr = len(pos2iid)

        # validate len(ids) == len(sizes)
        if len(pos2iid) != len(self.__pos2size):
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
        self.__parse_dimensions(json_data_dimension, json_data_roles, pos2iid)

        # TODO: parsing link

        self.__compute_pos2mult()
        self.__valid = True

    def __parse_dimensions(self, json_data_dimension, json_data_roles, pos2iid):
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
        self.__pos2dim = self.__dim_nr * [None]
        for dpos, dname in enumerate(pos2iid):
            dsize = self.__pos2size[dpos]

            if dname not in json_data_dimension:
                msg = "dataset '{}': malformed json: missing key {} in dimension".format(self.__name, dname)
                raise JsonStatException(msg)

            dimension = JsonStatDimension(dname, dsize, dpos, roles.get(dname))
            dimension.from_json(json_data_dimension[dname])
            self.__did2dim[dname] = dimension
            self.__pos2dim[dpos] = dimension
            if dimension.label is not None:
                self.__lbl2dim[dimension.label] = dimension

    def __compute_pos2mult(self):
        acc = 1
        self.__pos2mult = self.__dim_nr * [1]
        i = self.__dim_nr - 2
        while i >= 0:
            acc = acc * self.__pos2size[i + 1]
            self.__pos2mult[i] = acc
            i -= 1
