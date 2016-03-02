# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals


class IstatDimension:
    def __init__(self, name, pos, json_data):
        self.__name = name
        self.__pos = pos
        self.__desc2cod = {}
        self.__cod2desc = {}

        # parse json_data
        if json_data is not None:
            for i in json_data:
                cod = i['Cod']
                desc = i['Desc'].strip()
                self.__desc2cod[desc] = cod
                self.__cod2desc[cod] = desc

    def name(self):
        """the name of the istat dimension"""
        return self.__name

    def pos(self):
        """ position into the dataset"""
        return self.__pos

    def cod2desc(self, spec):
        if spec in self.__cod2desc:
            return self.__cod2desc[spec]
        else:
            return None

    def desc2cod(self, spec):
        if spec in self.__desc2cod:
            return self.__desc2cod[spec]
        else:
            return None

    def values_as_str(self):
        out = "("
        comma = False
        for item in self.__cod2desc.items():
            code = item[0]
            description = item[1]
            if comma: out += ", "
            out += "{}:'{}'".format(code, description)
            comma = True
        out += ")"
        return out

    def __str__(self):
        out = "'{}' {}".format(self.__name, self.values_as_str())
        return out

    def __repr__(self):
        """used by ipython to make a better representation"""
        return self.__str__()

    def info(self):
        print(self)
