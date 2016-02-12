# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals

# jsonstat
import jsonstat
#from jsonstat.collection import JsonStatCollection

# jsonstat-istat
from istat_exception import IstatException
from istat_dimension import IstatDimension


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

        self.__name2pos = None
        self.__pos2dim = None
        self.__name2dim = None

    def name(self):
        """
        the name of this dataset
        :return:
        """
        return self.__dataset['Desc']

    def cod(self):
        """
        return the code of this dataset
        :return: code
        """
        return self.__dataset['Cod']

    def __str__(self):
        out = "{}({}):{}".format(self.cod(), self.nrdim(), self.name())
        return out

    def __repr__(self):
        """
        used by ipython to make a better representation
        """
        return self.__str__()

    def info(self):
        print(self)

    def info_dimensions(self):
        """
        print info about dimensions of this dataset
        """
        for i, dim in enumerate(self.__pos2dim):
            print("dim {} {}".format(i, dim.__str__()))

    def nrdim(self):
        if self.__name2pos is None:
            self.__download_dimensions()
        return len(self.__pos2dim)

    def dimensions(self):
        """
        Get list of dimensions
        :return:
        """
        if self.__name2pos is None:
            self.__download_dimensions()
        return self.__name2dim.values()

    def dimension(self, spec):
        """
        Get dimension according to spec
        :param spec: can be a int or a string
        :return: a IstatDimension instance
        """
        if self.__name2pos is None:
            self.__download_dimensions()
        if type(spec) == int:
            return self.__pos2dim[spec]
        return self.__name2dim[spec]

    def getvalues(self, spec, rtype=jsonstat.JsonStatCollection):
        """
        get values by dimensions
        :param spec: it is a string for ex. "1,6,9,0,0"
        :param type:
        :return: if type is JsonStatCollection return an istance of JsonStatCollection
          otherwise return a json structure representing the istat dataset
        """
        if type(spec) == dict:
            a = len(self.__pos2dim) * [0]
            for (name, value) in spec.items():
                d = self.dimension(name)
                a[d.pos()] = value
            spec = ",".join(map(str, a))

        json_data = self.__istat_helper.datajson(self.__dataset['Cod'], spec, show=False)

        if rtype == jsonstat.JsonStatCollection:
            collection = jsonstat.JsonStatCollection()
            collection.from_json(json_data)
            return collection
        elif rtype == "json":
            return json_data

        raise IstatException("unknow type {}".format(rtype))

    def __download_dimensions(self):
        """
        downloads information about dimensions from the istat
        """
        json_data = self.__istat_helper.dim(self.__dataset['Cod'], show=False)
        if json_data is None:
            msg = "cannot retrieve info for dataset: {}".format(self.__dataset)
            raise IstatException(msg)

        self.__name2dim = {}
        self.__pos2dim = len(json_data) * [None]
        for pos, item in enumerate(json_data.items()):
            name = item[0].strip()
            json_dimension = item[1]
            self.__name2dim[name] = IstatDimension(name, pos, json_dimension)
            self.__pos2dim[pos] = self.__name2dim[name]
