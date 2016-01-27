# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import sys

# jsonstat
from jsonstat.istat.istat_helper import IstatHelper
from jsonstat.istat.istat_area import IstatArea


class Istat:
    """
    Represent root of all dataseries
    """

    def __init__(self, cache_dir="istat_cached", lang=1):
        """
        Initialize Istat class.
        :param cache_dir: where to store the cached file
        :param lang: 1=english, otherwise italian
        """
        self.__istat_helper = IstatHelper(cache_dir, lang)
        self.__id2area = None
        self.__name2area = None

    def area(self, spec):
        """
        get a IstatArea by name or id
        :param spec: can be a string or an int
        :return: a IstatArea
        """
        if self.__id2area is None:
            self.__download_areas()
        if type(spec) is str:
            return self.__name2area[spec]
        # python2 has also 'unicode' string type other than native string 'str' type
        elif sys.version_info < (3,) and type(spec) is unicode:
            return self.__name2area[spec]
        else:
            return self.__id2area[spec]

    def areas(self):
        if self.__id2area is None:
            self.__download_areas()
        return self.__id2area.values()

    def __download_areas(self):
        self.__id2area = {}
        self.__name2area = {}
        json_data = self.__istat_helper.area(False)
        for area in json_data:
            a = IstatArea(self.__istat_helper, area)
            self.__id2area[area['Id']] = a
            self.__name2area[area['Desc']] = a

