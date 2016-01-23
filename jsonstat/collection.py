# -*- coding: utf-8 -*-
# This file is part of jsonstat.py

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import sys
import json

# jsonstat
from jsonstat.dataset import JsonStatDataSet


class JsonStatCollection:
    """
    Represent a jsonstat collection.
    It contain one or more dataset.
    """
    def __init__(self):
        self.__url = None
        self.__name2dataset = {}
        self.__pos2dataset = None

    def dataset(self, spec):
        """
        returns a dataset beloging to the collection
        :param spec: can be:
                    - the name of collection (string) for jsonstat v1
                    - an integer (for jsonstat v2)
        :return:
        """
        # for python3 str == unicode
        if type(spec) is str:
            return self.__name2dataset[spec]
        # python2 has also unicode string type and native string 'str' type
        elif sys.version_info < (3,) and type(spec) is unicode:
            return self.__name2dataset[spec]
        elif type(spec) is int:
            return self.__pos2dataset[spec]
        raise ValueError()

    def __str__(self):
        out = ""
        for i in self.__name2dataset.values():
            out += "dataset: '{}'\n".format(i.name())
        return out

    def info(self):
        """
        print some info about this collection
        """
        print(self)

    def from_file(self, filename):
        """
        initialize this collection from file
        :param filename: name containing a jsonstat
        """
        with open(filename) as f:
            json_string = f.read()
            self.from_string(json_string)

    def from_string(self, json_string):
        """
        initialize this collection from a string
        :param json_string:
        """
        json_data = json.loads(json_string)
        self.from_json(json_data)

    def from_json(self, json_data):
        """
        initialize this collection from a json structure
        :param json_data:
        """

        if "version" in json_data:
            self.__from_json_v2(json_data)
        else:
            # jsonstat version 1.0
            self.__from_json_v1(json_data)

    def __from_json_v1(self, json_data):
        """
        parse a jsonstat version 1
        :param json_data: json structure
        """
        #         parser = ijson.parse(StringIO(json_string))
        # name2pos = {}
        # i = 0
        # for prefix, event, value in parser:
        #     # print prefix,event,value
        #     if prefix == '' and event =='map_key':
        #         # print "{}: {}".format(i, value)
        #         name2pos[value] = i
        #         i += 1
        for ds in json_data.items():
            dataset_name = ds[0]
            dataset_json = ds[1]

            dataset = JsonStatDataSet(dataset_name)
            dataset.from_json(dataset_json)
            self.__name2dataset[dataset_name] = dataset

    def __from_json_v2(self, json_data):
        """
        parse a jsonstat version 2
        :param json_data: json structure
        """
        # jsonstat version 2.0
        # "version" : "2.0",
        # "class" : "collection",
        # "href" : "http://json-stat.org/samples/oecd-canada-col.json",
        # "label" : "OECD-Canada Sample Collection",
        # "updated" : "2015-12-24",
        json_data_ds = json_data["link"]["item"]
        self.__pos2dataset = len(json_data_ds) * [None]
        for pos, ds in enumerate(json_data_ds):
            dataset = JsonStatDataSet()
            dataset.from_json(ds,version=2)
            self.__pos2dataset[pos] = dataset
