# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals

# istat
from istat_dataset import IstatDataset
from istat_exception import IstatException


class IstatArea:
    """
    Represents a Area. An Area contains a list of dataset.
    Instances of this class are build only by Istat class
    """
    def __init__(self, istat_helper, iid, cod, desc):
        self.__istat_helper = istat_helper
        self.__iid = iid
        self.__cod = cod
        self.__desc = desc
        self.__cod2dataset = None

    def iid(self):
        """
        returns the id of the area
        """
        return self.__iid

    def cod(self):
        """
        returns name of the area
        """
        return self.__cod

    def desc(self):
        """
        returns name of the area
        """
        return self.__desc

    def __str__(self):
        out = "{}:{}".format(self.__cod, self.__desc)
        return out

    def __repr__(self):
        """
        used by ipython to make a better representation
        """
        return self.__str__()

    def info(self):
        """
        print some info about the area
        """
        print(self)

    def dataset(self, spec):
        """
        get a instance of IstatDataset by spec
        :param spec: code of the dataset
        :return: IstatDataset instance
        """
        if self.__cod2dataset is None:
            self.__download_datasets()
        return self.__cod2dataset[spec]

    def datasets(self):
        """
        Return a list of IstatDataset
        """
        if self.__cod2dataset is None:
            self.__download_datasets()
        return self.__cod2dataset.values()

    def __download_datasets(self):
        """
        download a json_dataset using istat_helper
        """
        self.__cod2dataset = {}
        json_data = self.__istat_helper.dslist(self.__iid, show=False)
        if json_data is not None:
            for json_dataset in json_data:
                try:
                    dataset = IstatDataset(self.__istat_helper, json_dataset)
                    dataset.dimensions() # force download dimensions
                    self.__cod2dataset[json_dataset['Cod']] = dataset
                except IstatException:
                    # ignore istatexception for dataset that cannot retrieve dimensions
                    pass
        else:
            msg = "IstatArea area {}: cannot retrieve datasets".format(self.__area)
            raise IstatException(msg)

