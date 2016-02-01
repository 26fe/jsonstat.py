# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals

# jsonstat
from jsonstat.istat.istat_dimension import IstatDimension
from jsonstat.istat.istat_exception import IstatException


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

    def dimension(self, pos):
        if self.__name2pos is None:
            self.__download_dimensions()
        return self.__pos2dim[pos]

    def dimensions(self):
        if self.__name2pos is None:
            self.__download_dimensions()
        return self.__name2dim.values()

    def getvalues(self, dim):
        """
        get values by dimensions
        :param dim: it is a string for ex. "1,6,9,0,0"
        :return: json structure representing dataset
        """
        # TODO: returning a JsonStatCollection
        json_data = self.__istat_helper.datajson(self.__dataset['Cod'], dim, show=False)
        return json_data

    def __download_dimensions(self):
        """
        download information about dimensions from the istat
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
            self.__name2dim[name] = IstatDimension(name, json_dimension)
            self.__pos2dim[pos] = self.__name2dim[name]

        # self.__name2pos = mame2pos
        # self.__pos2dim = len(mame2pos) * [None]
        # for item in mame2pos.items():
        #     pos = item[1]
        #     name = item[0]
        #     self.__pos2dim[pos] = self.__name2dim[name]
