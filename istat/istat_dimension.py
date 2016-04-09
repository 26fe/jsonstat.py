# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals


class IstatDimension:
    """Represents a IstatDimension (it is different from JsonStat Dimension"""
    def __init__(self, name, pos, json_data):
        self.__name = name
        self.__pos = pos

        self.__pos2cod = []
        self.__desc2cod = {}
        self.__cod2desc = {}

        # parse json_data
        if json_data is not None:
            for pos, item in enumerate(json_data):
                cod = item['Cod']
                desc = item['Desc'].strip()
                self.__pos2cod.append(cod)
                self.__desc2cod[desc] = cod
                self.__cod2desc[cod] = desc

    @property
    def name(self):
        """the name of the istat dimension"""
        return self.__name

    @property
    def pos(self):
        """position into the dataset"""
        return self.__pos

    def __len__(self):
        """returns the number of categories"""
        return len(self.__cod2desc)

    def pos2cod(self, pos):
        return self.__pos2cod[pos]

    def cod2desc(self, spec):
        """returns the description corresponding to the cod"""
        if spec in self.__cod2desc:
            return self.__cod2desc[spec]
        return None

    def desc2cod(self, spec):
        """returns the code corresponding to the description"""
        if spec in self.__desc2cod:
            return self.__desc2cod[spec]
        return None

    def values_as_str(self, show_values=0):
        out = ""
        comma = False
        for pos, item in enumerate(self.__cod2desc.items()):
            cod = item[0]
            desc = item[1]
            if comma: out += ", "
            out += "{}:'{}'".format(cod, desc)
            comma = True
            if show_values != 0:
                show_values -= 1
                if show_values == 0 and pos != len(self.__pos2cod):
                    out += " ..."
                if show_values == 0:
                    break
        return out

    def __str__(self):
        out = "'{}' ({})".format(self.__name, self.values_as_str())
        return out

    def __repr__(self):
        """used by ipython to make a better representation"""
        return self.__str__()

    def info(self):
        print(self)
