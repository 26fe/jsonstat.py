# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
from collections import OrderedDict
import dateutil.parser
import json

# packages
import terminaltables

# jsonstat
from jsonstat.dataset import JsonStatDataSet
from jsonstat.utility import lst2html


class JsonStatCollection:
    """Represents a jsonstat collection.

    It contains one or more datasets.

    >>> import os, jsonstat  # doctest: +ELLIPSIS
    >>> filename = os.path.join(jsonstat.__fixtures_dir, "www.json-stat.org", "oecd-canada-col.json")
    >>> collection = jsonstat.from_file(filename)
    >>> len(collection)
    2
    >>> collection
    JsonstatCollection contains the following JsonStatDataSet:
    +-----+-----------------------------------------------------+
    | pos | dataset                                             |
    +-----+-----------------------------------------------------+
    | 0   | 'Unemployment rate in the OECD countries 2003-2014' |
    | 1   | 'Population by sex and age group. Canada. 2012'     |
    +-----+-----------------------------------------------------+

    """

    def __init__(self):
        self.__href = None
        self.__label = None
        self.__updated = None

        self.__name2dataset = {}  # str -> dataset
        self.__pos2dataset = []  # int -> dataset

    def __len__(self):
        """the number of dataset contained in this collection"""
        return len(self.__pos2dataset)

    def dataset(self, spec):
        """select a dataset belonging to the collection

        :param spec: can be

            - the name of collection (string) for jsonstat v1
            - an integer (for jsonstat v1 and v2)

        :returns: a JsonStatDataSet object
        """

        if type(spec) is int:
            return self.__pos2dataset[spec]
        return self.__name2dataset[spec]

    def __to_table(self):
        lst = [["pos", "dataset"]]
        for i, dataset in enumerate(self.__pos2dataset):
            row = [str(i), "'" + dataset.name + "'"]
            lst.append(row)
        return lst

    def __str__(self):
        out = "JsonstatCollection contains the following JsonStatDataSet:\n"
        lst = self.__to_table()
        table = terminaltables.AsciiTable(lst)
        out += table.table
        return out

    def __repr__(self):
        return self.__str__()

    def _repr_html_(self):
        """used by jupyter to make a better representation into notebooks"""
        html = "JsonstatCollection contains the following JsonStatDataSet:</br>"
        lst = self.__to_table()
        html += lst2html(lst)
        return html

    #
    # parsing methods
    #
    def from_file(self, filename):
        """initialize this collection from a file
        It is better to use :py:meth:`jsonstat.from_file`

        :param filename: name containing a jsonstat
        :returns: itself to chain call
        """
        with open(filename) as f:
            json_string = f.read()
            self.from_string(json_string)
        return self

    def from_string(self, json_string):
        """Initialize this collection from a string
        It is better to use :py:meth:`jsonstat.from_string`

        :param json_string: string containing a json
        :returns: itself to chain call
        """
        json_data = json.loads(json_string, object_pairs_hook=OrderedDict)
        self.from_json(json_data)
        return self

    def from_json(self, json_data):
        """initialize this collection from a json structure
        It is better to use :py:meth:`jsonstat.from_json`

        :param json_data: data structure (dictionary) representing a json
        :returns: itself to chain call
        """

        if "version" in json_data:
            self._from_json_v2(json_data)
        else:
            # jsonstat version 1.0
            self._from_json_v1(json_data)
        return self

    def _from_json_v1(self, json_data):
        """parse a jsonstat version 1

        .. warning::

            this is an internal library function (it is not public api)

        :param json_data: json structure

        json_data example::

            {
                "dataset1" : {...}
                "dataset2" : {...}
            }

        """
        for dataset_name, dataset_json in json_data.items():
            dataset = JsonStatDataSet(dataset_name)
            dataset.from_json(dataset_json)
            self.__name2dataset[dataset_name] = dataset
            self.__pos2dataset.append(dataset)

    def _from_json_v2(self, json_data):
        """parse a jsonstat version 2

        .. warning::

            this is an internal library function (it is not public api)

        :param json_data: json structure


        json_data example::

            "version" : "2.0",
            "class" : "collection",
            "href" : "http://json-stat.org/samples/collection.json",
            "label" : "JSON-stat Dataset Sample Collection",
            "updated" : "2015-07-02",
            "link" : {
               "item" : [
                    {},
                    {},
                ]
        }

        """

        if "href" in json_data:
            self.__href = json_data["href"]

        if "label" in json_data:
            self.__label = json_data["label"]

        if "updated" in json_data:
            self.__updated = dateutil.parser.parse(json_data["updated"])

        json_data_ds = json_data["link"]["item"]
        self.__pos2dataset = len(json_data_ds) * [None]
        for pos, ds in enumerate(json_data_ds):
            dataset = JsonStatDataSet()
            dataset._from_json_v2(ds)
            self.__pos2dataset[pos] = dataset
