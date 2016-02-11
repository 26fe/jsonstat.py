# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
from collections import OrderedDict
import json

#jsonstat
from jsonstat.collection import JsonStatCollection
from jsonstat.dataset import JsonStatDataSet
from jsonstat.dimension import JsonStatDimension
from jsonstat.exceptions import JsonStatMalformedJson


def from_file(filename):
    """
    read a file containing a jsonstat format and returns the appropriate object
    :param filename: name containing a jsonstat
    :return a JsonStatCollection, JsonStatDataset or JsonStatDimension object
    """
    with open(filename) as f:
        json_string = f.read()
        return from_string(json_string)


def from_string(json_string):
    """
    parse a jsonstat string and returns the appropriate object
    :param json_string: string containing a json
    :return a JsonStatCollection, JsonStatDataset or JsonStatDimension object
    """
    json_data = json.loads(json_string, object_pairs_hook=OrderedDict)
    return from_json(json_data)

def from_json(json_data):
    """
    transform a json structure into jsonstat library object
    :param json_data: data structure (dictionary) representing a json
    :return a JsonStatCollection, JsonStatDataset or JsonStatDimension object
    """
    o = None
    if "version" in json_data:
        # if version present assuming version 2 of jsonstat format
        if "class" in json_data:
            if json_data["class"] == "collection":
                o = JsonStatCollection()
                o.from_json_v2(json_data)
            elif json_data["class"] == "dataset":
                o = JsonStatDataSet()
                o.from_json_v2(json_data)
            elif json_data["class"] == "dimension":
                o = JsonStatDimension()
                o.from_json(json_data)
            else:
                msg = "unknow class {}".format(json_data["class"])
                raise JsonStatMalformedJson(msg)

    else:
        # if version is not present assuming version 1.0 of jsonstat format
        o = JsonStatCollection()
        o.from_json_v1(json_data)
    return o
