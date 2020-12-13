# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2021 gf <gf@26fe.com>
# See LICENSE file

# stdlib
import os
from os.path import isfile, join

# external modules
import pytest

# jsonstat
import jsonstat


def test_parse_collection():
    json_string_v1_one_dataset = """
        {
            "oecd" : {
                "value": [1],
                "dimension" : {
                    "id": ["one"],
                    "size": [1],
                    "one": { "category": { "index":{"2010":0}} }
                }
            }
        }
        """
    ret = jsonstat.from_string(json_string_v1_one_dataset)
    assert isinstance(ret, jsonstat.JsonStatCollection)

    json_string_v1_two_datasets = """
        {
            "oecd" : {
                "value": [1],
                "dimension" : {
                    "id": ["one"],
                    "size": [1],
                    "one": { "category": { "index":{"2010":0}} }
                }
            },
            "canada" : {
                "value": [1],
                "dimension": {
                    "id": ["one"],
                    "size": [1],
                    "one": { "category": { "index":{"2010":0}} }
                }
            }
        }
        """
    ret = jsonstat.from_string(json_string_v1_two_datasets)
    assert isinstance(ret, jsonstat.JsonStatCollection)


def test_parse_dataset():
    f = os.path.join(jsonstat._examples_dir, "www.json-stat.org", "canada.json")
    dataset = jsonstat.from_file(f)
    assert dataset is not None
    assert isinstance(dataset, jsonstat.JsonStatDataSet)
    assert 120 == len(dataset)


def test_parse_dimension():
    json_string_dimension = """
        {
            "version" : "2.0",
            "class" : "dimension",
            "label" : "sex",
            "category" : {
                "index" : ["T", "M", "F"],
                "label" : {
                    "T" : "total",
                    "M" : "male",
                    "F" : "female"
                }
            }
        }
        """
    ret = jsonstat.from_string(json_string_dimension)
    assert isinstance(ret, jsonstat.JsonStatDimension)


def test_parsing_json_stat_org_files():
    example_jsonstat_org_dir = os.path.join(jsonstat._examples_dir, "www.json-stat.org")
    for f in os.listdir(example_jsonstat_org_dir):
        jsonstat_file = join(example_jsonstat_org_dir, f)
        if isfile(jsonstat_file) and jsonstat_file.endswith(".json"):
            # print("parsing {}".format(jsonstat_file))
            ret = jsonstat.from_file(jsonstat_file)
            msg = "parsing {}".format(jsonstat_file)
            assert ret is not None, msg
