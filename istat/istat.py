# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import sys

# jsonstat
from istat_helper import IstatHelper
from istat_area import IstatArea


class Istat:
    """
    Represent the root of all Istat dataseries
    """

    def __init__(self, cache_dir="istat_cached", lang=1):
        """
        Initialize Istat class.
        :param cache_dir: where to store the cached file
        :param lang: 1=english, otherwise italian
        """
        self.__istat_helper = IstatHelper(cache_dir, lang)
        self.__id2area = None
        self.__cod2area = None
        self.__desc2area = None

    def areas(self):
        """
        Get a list of all areas
        :return: list of IstatArea instances
        """
        if self.__id2area is None:
            self.__download_areas()
        return self.__id2area.values()

    def area(self, spec):
        """
        get a IstatArea by name or id
        :param spec: can be a string (for code or desc) or an int (for id)
        :return: a IstatArea istance
        """
        if self.__id2area is None:
            self.__download_areas()
        if type(spec) is str:
            if spec in self.__cod2area: return self.__cod2area[spec]
            if spec in self.__desc2area: return self.__desc2area[spec]
        # python2 has also 'unicode' string type other than native string 'str' type
        elif sys.version_info < (3,) and type(spec) is unicode:
            if spec in self.__cod2area: return self.__cod2area[spec]
            if spec in self.__desc2area: return self.__desc2area[spec]
        else:
            spec = int(spec) # try to convert into int
            return self.__id2area[spec]

    def dataset(self, spec_area, spec_dataset):
        """
        Returns an IstatDataset
        :param spec_area: selector for an IstatArea
        :param spec_dataset: selector for an IstatDataset that belong to the spec_area dataset
        :return: an instance of IstatDataset
        """
        a = self.area(spec_area)
        ds = a.dataset(spec_dataset)
        return ds

    def __download_areas(self):
        self.__id2area = {}
        self.__cod2area = {}
        self.__desc2area = {}
        json_data = self.__istat_helper.area(False)
        for area in json_data:
            iid = int(area['Id'])  # try to convert into int
            cod = area['Cod']
            desc = area['Desc']
            if iid in self.__id2area:
                continue
            istat_area = IstatArea(self.__istat_helper, iid, cod, desc)
            self.__id2area[iid] = istat_area
            self.__cod2area[cod] = istat_area
            self.__desc2area[desc] = istat_area

