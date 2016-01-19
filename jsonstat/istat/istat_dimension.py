# This file is part of jsonstat.py

# stdlib
from __future__ import print_function
# jsonstat


class IstatDimension:
    def __init__(self, name, json_data):
        # print json_data
        self.__name = name
        self.__json_data = json_data
        self.__desc2cod = {}
        self.__cod2desc = {}
        if json_data is not None:
            for i in json_data:
                cod = i['Cod']
                desc = i['Desc']
                self.__desc2cod[desc] = cod
                self.__cod2desc[cod] = desc

    def name(self):
        return self.__name

    def desc2cod(self, str):
        pass

    def info(self):
        print(self.__name)
        # print self.json_data
        for i in self.__cod2desc.items():
            print("  {}:{}".format(i[0], i[1]))