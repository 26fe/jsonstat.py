# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
from collections import OrderedDict
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
        self.__pos2dataset = []

    def dataset(self, spec):
        """
        returns a dataset beloging to the collection
        :param spec: can be:
                    - the name of collection (string) for jsonstat v1
                    - an integer (for jsonstat v2)
        :return: a dataset
        """

        # In Python2, str == bytes.
        # In Python3, str means unicode (bytes remains unchanged),
        #             while unicode is not defined anymore

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
        for i, dataset in enumerate(self.__pos2dataset):
            out += "{}: dataset '{}'\n".format(i, dataset.name())
        return out

    def __repr__(self):
        """
        used by ipython to make a better representation
        """
        return self.__str__()

    def info(self):
        """
        print some info about this collection
        """
        print(self)

    def from_file(self, filename):
        """
        initialize this collection from a file
        :param filename: name containing a jsonstat
        :return itself to chain call
        """
        with open(filename) as f:
            json_string = f.read()
            self.from_string(json_string)
        return self

    def from_string(self, json_string):
        """
        initialize this collection from a string
        :param json_string: string containing a json
        :return itself to chain call
        """
        json_data = json.loads(json_string, object_pairs_hook=OrderedDict)
        self.from_json(json_data)
        return self

    def from_json(self, json_data):
        """
        initialize this collection from a json structure
        :param json_data: data structure (dictionary) representing a json
        :return itself to chain call
        """

        if "version" in json_data:
            self.from_json_v2(json_data)
        else:
            # jsonstat version 1.0
            self.from_json_v1(json_data)
        return self

    # TODO: this is meant of internal function of jsonstat not public api
    def from_json_v1(self, json_data):
        """
        parse a jsonstat version 1
        :param json_data: json structure
        """

        for ds in json_data.items():
            dataset_name = ds[0]
            dataset_json = ds[1]

            dataset = JsonStatDataSet(dataset_name)
            dataset.from_json(dataset_json)
            self.__name2dataset[dataset_name] = dataset
            self.__pos2dataset.append(dataset)

    # TODO: this is meant of internal function of jsonstat not public api
    def from_json_v2(self, json_data):
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
