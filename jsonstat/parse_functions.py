# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
from collections import OrderedDict
import json

# jsonstat
from jsonstat.exceptions import JsonStatMalformedJson
from jsonstat.downloader import *
from jsonstat.collection import JsonStatCollection
from jsonstat.dataset import JsonStatDataSet
from jsonstat.dimension import JsonStatDimension


def from_file(filename):
    """read a file containing a jsonstat format and returns the appropriate object

    :param filename: name containing a jsonstat
    :returns: a JsonStatCollection, JsonStatDataset or JsonStatDimension object

    ::

        filename = os.path.join(self.fixture_dir, "oecd-canada.json")
        collection = jsonstat.from_file(filename)

    """
    with open(filename) as f:
        json_string = f.read()
        return from_string(json_string)


def from_string(json_string):
    """parse a jsonstat string and returns the appropriate object

    :param json_string: string containing a json
    :returns: a JsonStatCollection, JsonStatDataset or JsonStatDimension object
    """
    json_data = json.loads(json_string, object_pairs_hook=OrderedDict)
    return from_json(json_data)


def from_json(json_data):
    """transform a json structure into jsonstat objects hierarchy

    :param json_data: data structure (dictionary) representing a json
    :returns: a JsonStatCollection, JsonStatDataset or JsonStatDimension object

    ::

        json_data = json.loads(json_string, object_pairs_hook=OrderedDict)
        jsonstat.from_json(json_data)
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


# global module variable (simulate a singleton)
__downloader__ = None


def cache_dir(cached_dir='', time_to_live=None):
    """Manage the directory ``cached_dir`` where to store downloaded files

    without parameter return the ``cached_dir`` directory
    with a parameters set the directory

    :param cached_dir:
    :param time_to_live:
    """
    global __downloader__
    if cache_dir == '' and time_to_live is None:
        if __downloader__ is None:
            return __downloader__.cache_dir()

    __downloader__ = Downloader(cached_dir, time_to_live)
    return __downloader__.cache_dir()


def download(url, pathname=None):
    """download a url into a file ``pathname``

    :param url:
    :param pathname: where to store the url
    :return: the content of url
    """
    global __downloader__
    if __downloader__ is None:
        __downloader__ = Downloader()

    if pathname is None:
        return __downloader__.download(url)
    else:
        d = Downloader(os.path.dirname(pathname))
        return d.download(url, os.path.basename(pathname))


# TODO: pathname could be None so don't save on disk
def from_url(url, pathname=None):
    """download a url into a file ``pathname`` and returns the content of the url

    :param url:
    :param pathname: where to store the url
    :returns: the content of url
    """
    json_string = download(url, pathname)
    return from_string(json_string)
