# -*- coding: utf-8 -*-
#  This file is part of jsonstat.py

# stdlib
from __future__ import print_function
from __future__ import unicode_literals

# jsonstat
from jsonstat.istat.istat_dimension import IstatDimension
from jsonstat.istat.istat_exception import IstatException


class IstatDataset:
    def __init__(self, istat_helper, dataset):
        self.__istat_helper = istat_helper
        self.__dataset = dataset
        self.__name2pos = None
        self.__pos2dim = None
        self.__name2dim = None

    def name(self):
        return self.__dataset['Desc']

    def cod(self):
        return self.__dataset['Cod']

    def __str__(self):
        out = "{}:{}".format(self.__dataset['Cod'], self.__dataset['Desc'])
        return out

    def info(self):
        print(self)

    def info_dimensions(self):
        i = 0
        for d in self.__pos2dim:
            print("pos: {}".format(i))
            d.info()
            i += 1

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
        # dim = "1,6,9,0,0"
        json_data = self.__istat_helper.datajson(self.__dataset['Cod'], dim, show=False)
        return json_data

    def __download_dimensions(self):
        (mame2pos, json_data) = self.__istat_helper.dim(self.__dataset['Cod'], show=False)
        if json_data is None:
            msg = "cannot retrieve info for dataset: {}".format(self.__dataset)
            raise IstatException(msg)


        # print u"dataset: '{}' '{}' dim: {}".format(self.dataset['Cod'], self.dataset['Desc'], len(json_data))
        self.__name2dim = {}
        for item in json_data.items():
            name = item[0]
            json_dimension = item[1]
            self.__name2dim[name] = IstatDimension(name, json_dimension)

        self.__name2pos = mame2pos
        self.__pos2dim = len(mame2pos) * [None]
        for item in mame2pos.items():
            pos = item[1]
            name = item[0]
            self.__pos2dim[pos] = self.__name2dim[name]
