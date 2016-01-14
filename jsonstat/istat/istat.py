#
# stdlib
#
import os

#
# jsonstat
#
import jsonstat
from jsonstat.istat.istat_helper import IstatHelper
from jsonstat.istat.istat_area import IstatArea

class Istat:
    """
    Represent root of all dataseries
    """

    def __init__(self, cache_dir="istat_cached",lang=1):
        self.__istat_helper = IstatHelper(cache_dir, lang)
        self.__id2area = None
        self.__name2area = None

    def area(self, spec):
        """
        get a IstatArea by name or id
        :param spec:
        :return:
        """
        if self.__id2area is None:
            self.__download_areas()
        if type(spec) is str:
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

