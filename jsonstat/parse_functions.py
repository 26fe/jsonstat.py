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
    """read a file containing a jsonstat format and return the appropriate object

    :param filename: file containing a jsonstat
    :returns: a JsonStatCollection, JsonStatDataset or JsonStatDimension object

    example

    >>> import os, jsonstat
    >>> filename = os.path.join(jsonstat.__fixtures_dir, "www.json-stat.org", "oecd-canada-col.json")
    >>> o = jsonstat.from_file(filename)
    >>> type(o)
    <class 'jsonstat.collection.JsonStatCollection'>
    """
    with open(filename) as f:
        json_string = f.read()
        return from_string(json_string)


def from_string(json_string):
    """parse a jsonstat string and return the appropriate object

    :param json_string: string containing a json
    :returns: a JsonStatCollection, JsonStatDataset or JsonStatDimension object
    """
    try:
        json_data = json.loads(json_string, object_pairs_hook=OrderedDict)
    except json.decoder.JSONDecodeError:
        raise JsonStatException("invalid json")
    return from_json(json_data)


def from_json(json_data):
    """transform a json structure into jsonstat objects hierarchy

    :param json_data: data structure (dictionary) representing a json
    :returns: a JsonStatCollection, JsonStatDataset or JsonStatDimension object

    >>> import json, jsonstat
    >>> from collections import OrderedDict
    >>> json_string_v1 = '''{
    ...                       "oecd" : {
    ...                         "value": [1],
    ...                         "dimension" : {
    ...                           "id": ["one"],
    ...                           "size": [1],
    ...                           "one": { "category": { "index":{"2010":0 } } }
    ...                         }
    ...                       }
    ...                     }'''
    >>> json_data = json.loads(json_string_v1, object_pairs_hook=OrderedDict)
    >>> jsonstat.from_json(json_data)
    JsonstatCollection contains the following JsonStatDataSet:
    +-----+---------+
    | pos | dataset |
    +-----+---------+
    | 0   | 'oecd'  |
    +-----+---------+

    """
    o = None
    if "version" in json_data:
        # if version present assuming version 2 of jsonstat format
        if "class" in json_data:
            if json_data["class"] == "collection":
                o = JsonStatCollection()
                o._from_json_v2(json_data)
            elif json_data["class"] == "dataset":
                o = JsonStatDataSet()
                o._from_json_v2(json_data)
            elif json_data["class"] == "dimension":
                o = JsonStatDimension()
                o.from_json(json_data)
            else:
                msg = "unknown class {}".format(json_data["class"])
                raise JsonStatMalformedJson(msg)

    else:
        # if version is not present assuming version 1.0 of jsonstat format
        o = JsonStatCollection()
        o._from_json_v1(json_data)
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
    """download a url and return the downloaded content``

    :param url: ex.: http://json-stat.org/samples/oecd-canada.json
    :param pathname: If ``pathname`` is defined the contents of the url
    will be stored into the file ``<cache_dir>/pathname``
    If ``pathname`` is None the filename will be automatic generated.
    If ``pathname`` is an absolute path cache_dir will be ignored.

    :returns: the contents of url

    To set dir where to store downloaded file
    see :py:meth:`jsonstat.cache_dir`.
    Cache expiration policy can be customized

    """
    global __downloader__
    if __downloader__ is None:
        __downloader__ = Downloader()

    if pathname is None:
        return __downloader__.download(url)
    elif not os.path.isabs(pathname):
        return __downloader__.download(url, pathname)
    else:
        tmp_cache_dir = os.path.dirname(pathname)
        d = Downloader(tmp_cache_dir)
        return d.download(url, os.path.basename(pathname))


def from_url(url, pathname=None):
    """download an url and return the downloaded content.

    see :py:meth:`jsonstat.download` for how to use pathname parameter.

    :param url: ex.: http://json-stat.org/samples/oecd-canada.json
    :param pathname: If ``pathname`` is defined the contents of the url
    will be stored into the file ``<cache_dir>/pathname``
    If ``pathname`` is None the filename will be automatic generated.
    If ``pathname`` is an absolute path cache_dir will be ignored.

    :returns: the contents of url

    To set dir where to store downloaded file
    see :py:meth:`jsonstat.cache_dir`.
    Cache expiration policy can be customized

    example:

    >>> import jsonstat
    >>> # cache_dir = os.path.normpath(os.path.join(jsonstat.__fixtures_dir, "json-stat.org"))
    >>> # download external content into the /tmp dir so next downloads can be faster
    >>> uri = 'http://json-stat.org/samples/oecd-canada.json'
    >>> jsonstat.cache_dir("/tmp")
    '/tmp'
    >>> o = jsonstat.from_url(uri)
    >>> print(o)
    JsonstatCollection contains the following JsonStatDataSet:
    +-----+----------+
    | pos | dataset  |
    +-----+----------+
    | 0   | 'oecd'   |
    | 1   | 'canada' |
    +-----+----------+

    """
    json_string = download(url, pathname)
    return from_string(json_string)


def validate(spec):
    try:
        import jsonschema
        import strict_rfc3339  # validate date-time format in jsonschema
    except ImportError:
        print("to validate install jsonschema and strict_rfc3339")
        return

    from jsonstat.schema import JsonStatSchema

    if not isinstance(spec, dict):
        json_data = json.loads(spec, object_pairs_hook=OrderedDict)
    else:
        json_data = spec
    if "version" not in json_data:
        raise JsonStatException("cannot validate jsonstat version < 2.0")
    # schema = JsonStatSchema()
    jsonstat_schema_url = "https://json-stat.org/format/schema/2.0/"
    contents = download(jsonstat_schema_url)
    schema = json.loads(contents)
    validator = jsonschema.Draft4Validator(schema, format_checker=jsonschema.FormatChecker())
    # validator.validate(json_data)
    errors = sorted(validator.iter_errors(json_data), key=lambda e: e.path)
    return len(errors) == 0
