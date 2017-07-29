# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import os
from io import StringIO

# external modules
import pytest

# jsonstat
import jsonstat


@pytest.fixture(scope='module')
def json_string_v1_one_dataset():
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
    return json_string_v1_one_dataset


@pytest.fixture(scope='module')
def json_string_v1_two_datasets():
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
    return json_string_v1_two_datasets


def test_one_dataset_to_str(json_string_v1_one_dataset):
    collection = jsonstat.JsonStatCollection()
    collection.from_string(json_string_v1_one_dataset)
    expected = [
        "JsonstatCollection contains the following JsonStatDataSet:\n",
        "+-----+---------+\n",
        "| pos | dataset |\n",
        "+-----+---------+\n",
        "| 0   | 'oecd'  |\n",
        "+-----+---------+"
    ]
    expected = ''.join(expected)
    assert expected == str(collection)


def test_two_datasets_to_str(json_string_v1_two_datasets):
    collection = jsonstat.JsonStatCollection()
    collection.from_string(json_string_v1_two_datasets)
    expected = (
        "JsonstatCollection contains the following JsonStatDataSet:\n"
        "+-----+----------+\n"
        "| pos | dataset  |\n"
        "+-----+----------+\n"
        "| 0   | 'oecd'   |\n"
        "| 1   | 'canada' |\n"
        "+-----+----------+"
    )
    assert expected == str(collection)


def test_parse_v1_from_string(json_string_v1_two_datasets):
    collection = jsonstat.JsonStatCollection()
    collection.from_string(json_string_v1_two_datasets)

    assert collection.dataset('oecd') is not None
    assert collection.dataset('canada') is not None


def test_parse_v1_from_file():
    filename = os.path.join(jsonstat._examples_dir, "www.json-stat.org", "oecd-canada.json")
    collection = jsonstat.JsonStatCollection()
    collection.from_file(filename)

    assert collection.dataset('oecd') is not None
    assert collection.dataset('canada') is not None

    oecd = collection.dataset("oecd")
    dim = oecd.dimension("concept")
    expected = (
        "+-----+-------+---------------------+\n"
        "| pos | idx   | label               |\n"
        "+-----+-------+---------------------+\n"
        "| 0   | 'UNR' | 'unemployment rate' |\n"
        "+-----+-------+---------------------+"
    )
    assert expected == dim.__str__()


def test_parse_v2_from_file():
    filename = os.path.join(jsonstat._examples_dir, "www.json-stat.org", "oecd-canada-col.json")
    collection = jsonstat.JsonStatCollection()
    collection.from_file(filename)

    oecd = collection.dataset(0)
    assert oecd is not None

    canada = collection.dataset(1)
    assert canada is not None
