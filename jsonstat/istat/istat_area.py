# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals

# jsonstat
from jsonstat.istat.istat_dataset import IstatDataset
from jsonstat.istat.istat_exception import IstatException


#
# Represent a Area. An Area contains dataset
#
class IstatArea:
    def __init__(self, istat_helper, area):
        self.__istat_helper = istat_helper
        self.__area = area
        self.__cod2dataset = None

    def name(self):
        """
        name of the area
        :return:
        """
        return self.__area['Desc']

    def __str__(self):
        out = "{}:{}".format(self.__area['Id'], self.__area['Desc'])
        return out

    def info(self):
        """
        print some info about the area
        :return:
        """
        print(self)

    def dataset(self, name):
        """
        get a IstatDataset by name
        :param name:
        :return:
        """
        if self.__cod2dataset is None:
            self.__download_datasets()
        return self.__cod2dataset[name]

    def datasets(self):
        """
        Return a list of datasets
        :return:
        """
        if self.__cod2dataset is None:
            self.__download_datasets()
        return self.__cod2dataset.values()

    def __download_datasets(self):
        self.__cod2dataset = {}
        json_data = self.__istat_helper.dslist(self.__area['Id'], show=False)
        if json_data is not None:
            # print "-------------------------"
            # print u"area: {} '{}' nr. dataset {}".format(self.area['Id'], self.area['Desc'], len(json_data))
            for dataset in json_data:
                # self.show_dim(dataset)
                # print dataset
                self.__cod2dataset[dataset['Cod']] = IstatDataset(self.__istat_helper, dataset)
        else:
            msg = "cannot retrieve info for area {}".format(self.__area)
            raise IstatException(msg)

