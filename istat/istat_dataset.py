# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals

# jsonstat
import jsonstat

# istat
from istat.istat_exception import IstatException
from istat.istat_dimension import IstatDimension
import istat.options


class IstatDatasetList(list):
    def _repr_html_(self):
        """returns an html string useful to show into ipython notebook"""

        html = "<table>"
        html += "<tr><th>cod</th><th>name</th><th>dim</th></tr>"
        for ds in self:
            html += "<tr>"
            html += "<td>{}</td>".format(ds.cod)
            html += "<td>{}</td>".format(ds.name)
            html += "<td>{}</td>".format(ds.nrdim())
            html += "</td>"
            html += "</tr>"
        html += "</table>"
        return html


class IstatDataset:
    def __init__(self, istat_helper, dataset):
        """
        Initialize this istat dataset. Dataset is child of Istat.
        This class must be only instanziated by Istat classes that belongs to
        :param istat_helper: used to download dataset
        :param dataset: it is the structure from which takes parameters
        """
        self.__istat_helper = istat_helper
        self.__dataset = dataset

        self.__name2dim = None  # dict
        self.__pos2dim = None  # array

    @property
    def cod(self):
        """returns the code of this dataset"""
        return self.__dataset['Cod']

    @property
    def name(self):
        """returns the name of this dataset"""
        return self.__dataset['Desc']

    def __len__(self):
        """ returns the number of dimensions"""
        self.__download_dimensions()
        return len(self.__name2dim)

    def __str__(self):
        out = "{}({}):{}".format(self.cod, self.nrdim(), self.name)
        return out

    def __repr__(self):
        """used by ipython to make a better representation"""
        return self.__str__()

    def _repr_html_(self):
        """prints info about dimension in html format

        :param show_values: number of values to show. If equals to 0 show all values
        :returns: html string
        """
        show_values = istat.options.display.max_rows
        html = "{}({}):{}</br>".format(self.cod, self.nrdim(), self.name)
        html += "<table>"
        html += "<tr><th>nr</th><th>name</th><th>nr. values</th>"
        if show_values == 0:
            html += "<th>values (alls values)</th></tr>"
        else:
            html += "<th>values (first {} values)</th></tr>".format(show_values)
        for i, dim in enumerate(self.__pos2dim):
            html += "<tr>"
            html += "<td>{}</td>".format(i)
            html += "<td>{}</td>".format(dim.name)
            html += "<td>{}</td>".format(len(dim))
            html += "<td>{}</td>".format(dim.values_as_str(show_values))
            html += "</td>"
            html += "</tr>"
        html += "</table>"
        return html

    def info(self):
        print(self)

    def info_dimensions(self):
        """print info about dimensions of this dataset"""
        for i, dim in enumerate(self.__pos2dim):
            print("dim {} {}".format(i, dim.__str__()))

    def nrdim(self):
        """returns the number of dimensions"""
        self.__download_dimensions()
        return len(self.__pos2dim)

    def dimensions(self):
        """Get list of dimensions

        :return: list of IstatDimension
        """
        self.__download_dimensions()
        return self.__name2dim.values()

    def dimension(self, spec):
        """Get dimension according to spec

        :param spec: can be a int or a string
        :return: an IstatDimension instance
        """
        self.__download_dimensions()
        if type(spec) == int:
            return self.__pos2dim[spec]
        return self.__name2dim[spec]

    def getvalues(self, spec, rtype=jsonstat.JsonStatCollection):
        """get values by dimensions

        :param spec: it is a string for ex. "1,6,9,0,0"
        :param type:

        :returns: if type is JsonStatCollection return an istance of JsonStatCollection
          otherwise return a json structure representing the istat dataset
        """
        if type(spec) == dict:

            dim_values_array = len(self.__pos2dim) * [0]
            for i, dim in enumerate(self.__pos2dim):
                # if the cardinality of IstatDimension is 1
                # use the unique value as default
                if len(dim) == 1:
                    dim_values_array[i] = dim.pos2cod(0)

            for (dim_name, value) in spec.items():
                dim = self.dimension(dim_name)
                # if cannot find the value in dimension keys
                # search value into the description
                if value != 0 and dim.cod2desc(value) is None:
                    if dim.desc2cod(value) is None:
                        msg = "unknown value '{}' for dimension '{}'".format(value, dim.name())
                        raise IstatException(msg)
                    value = dim.desc2cod(value)

                dim_values_array[dim.pos] = value
            spec = ",".join(map(str, dim_values_array))

        json_data = self.__istat_helper.datajson(self.__dataset['Cod'], spec, show=False)

        if rtype == jsonstat.JsonStatCollection:
            collection = jsonstat.JsonStatCollection()
            collection.from_json(json_data)
            return collection
        elif rtype == "json":
            return json_data

        raise IstatException("unknown type {}".format(rtype))

    def __download_dimensions(self):
        """downloads information about dimensions from the istat"""
        if self.__name2dim is not None:
            return

        json_data = self.__istat_helper.dim(self.__dataset['Cod'], show=False)
        if json_data is None:
            msg = "dataset {}: cannot retrieve dimensions info".format(self.__dataset)
            raise IstatException(msg)

        self.__name2dim = {}
        self.__pos2dim = len(json_data) * [None]
        for pos, item in enumerate(json_data.items()):
            name = item[0].strip()
            json_dimension = item[1]
            self.__name2dim[name] = IstatDimension(name, pos, json_dimension)
            self.__pos2dim[pos] = self.__name2dim[name]
