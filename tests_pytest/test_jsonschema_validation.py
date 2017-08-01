# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2017 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
# from __future__ import unicode_literals
import os
import json

# packages
import pytest
import jsonschema
import strict_rfc3339

# jsonstat
import jsonstat
from jsonstat.schema import JsonStatSchema


fixture_dir = os.path.join(os.path.dirname(__file__), "..", "tests", "fixtures")
schema = JsonStatSchema()


def validate(json_data, schemas):
    for s in schemas:
        # jsonschema.validate(json_data, s,  format_checker=jsonschema.FormatChecker())
        validator = jsonschema.Draft4Validator(s, format_checker=jsonschema.FormatChecker())
        # validator.validate(json_data)
        errors = sorted(validator.iter_errors(json_data), key=lambda e: e.path)
        if len(errors) != 0:
            print(errors)
            return False
    return True


def test_dimension1():
    # dimension.index as array
    jsonstat_string = {
        "version": "2.0",
        "class": "dimension",
        "label": "sex",
        "category":
            {
                "index": ["M", "F", "T"],
                "label": {
                    "M": "men",
                    "F": "women",
                    "T": "total"
                }
            }
    }
    schemas = [schema.dimension, schema.all]
    assert validate(jsonstat_string, schemas)


def test_dimension2():
    # dimension.child
    jsonstat_string = {
        "version": "2.0",
        "class": "dimension",
        "label": "activity status",
        "category": {
            "index": {
                "A": 0,
                "E": 1,
                "U": 2,
                "I": 3,
                "T": 4
            },
            "label": {
                "A": "active population",
                "E": "employment",
                "U": "unemployment",
                "I": "inactive population",
                "T": "population 15 years old and over"
            },
            "child": {
                "A": ["E", "U"],
                "T": ["A", "I"]
            }
        }
    }
    schemas = [schema.dimension, schema.all]
    assert validate(jsonstat_string, schemas)


def test_dimension3():
    # dimension.coordinates
    jsonstat_string = {
        "version": "2.0",
        "class": "dimension",
        "category": {
            "label": {
                "ISO-3166-2:TV": "Tuvalu"
            },
            "coordinates": {
                "ISO-3166-2:TV": [179.1995, -8.5199]
            }
        }
    }
    schemas = [schema.dimension, schema.all]
    assert validate(jsonstat_string, schemas)


def test_dimension4():
    json_data = {
        "version": "2.0",
        "class": "dimension",
        "label": "concepts",
        "category": {
            "index": {
                "POP": 0,
                "PERCENT": 1
            },
            "label": {
                "POP": "population",
                "PERCENT": "weight of age group in the population"
            },
            "unit": {
                "POP": {
                    "label": "thousands of persons",
                    "decimals": 1,
                    "type": "count",
                    "base": "people",
                    "multiplier": 3
                },
                "PERCENT": {
                    "label": "%",
                    "decimals": 1,
                    "type": "ratio",
                    "base": "per cent",
                    "multiplier": 0
                }
            }
        }
    }
    schemas = [schema.dimension, schema.all]
    assert validate(json_data, schemas)


def test_dataset1():
    # "required": ["version", "class", "value", "id", "size", "dimension"]

    jsonstat_data = {
        "version": "2.0",
        "class": "dataset",
        "updated": "2012-11-27",
        "id": ["concept", "area", "year"],
        "size": [1, 36, 12],
        "dimension": {
            "sex": {"label": "sex",
                    "category":
                        {
                            "index": ["M", "F", "T"],
                            "label": {
                                "M": "men",
                                "F": "women",
                                "T": "total"
                            }
                        }}},
        "value": []
    }
    schemas = [schema.dataset]
    # schema = [self.__schema.all]
    assert validate(jsonstat_data, schemas)


def test_dataset2():
    # dataset.role
    jsonstat_data = {
        "version": "2.0",
        "class": "dataset",
        "id": ["concept", "arrival_date", "departure_date", "origin", "destination"],
        "size": [1, 24, 24, 10, 10],
        "value": [1, 2, 3],
        "dimension": {},
        "role": {
            "time": ["arrival_date", "departure_date"],
            "geo": ["origin", "destination"],
            "metric": ["concept"]
        }
    }
    schemas = [schema.dataset, schema.all]
    assert validate(jsonstat_data, schemas)


def test_dataset3():
    # dataset.value null value
    jsonstat_string = """{
            "version": "2.0",
            "class": "dataset",
            "id": ["a"],
            "size": [1],
            "dimension": {},
            "value": [105.3, 104.3, null, 177.2]
        }"""
    jsonstat_data = json.loads(jsonstat_string)
    schemas = [schema.dataset, schema.all]
    schemas = [schema.dataset]
    assert validate(jsonstat_data, schemas)


def test_dataset4():
    # dataset.value as dict
    jsonstat_data = {
        "version": "2.0",
        "class": "dataset",
        "value": {"0": 1.3587, "18": 1.5849},
        "id": ["a"],
        "size": [1],
        "dimension": {},
    }
    schemas = [schema.dataset, schema.all]
    schemas = [schema.dataset]
    assert validate(jsonstat_data, schemas)


def test_dataset5():
    # dataset.status
    jsonstat_string = """{
            "version": "2.0",
            "class": "dataset",
            "value": [100, null, 102, 103, 104],
            "status": ["a", "m", "a", "a", "p"],
            "id": ["a"],
            "size": [1],
            "dimension": {}
        }"""
    jsonstat_data = json.loads(jsonstat_string)
    schemas = [schema.dataset, schema.all]
    schemas = [schema.all]
    assert validate(jsonstat_data, schemas)


def test_dataset6():
    # dataset.status
    jsonstat_data = {
        "version": "2.0",
        "class": "dataset",
        "value": [100, 99, 102, 103, 104],
        "status": "e",
        "id": ["a"],
        "size": [1],
        "dimension": {}
    }
    schemas = [schema.dataset, schema.all]
    schemas = [schema.all]
    assert validate(jsonstat_data, schemas)


def test_dataset7():
    # dataset.status
    jsonstat_string = """{
            "version": "2.0",
            "class": "dataset",
            "value": [100, null, 102, 103, 104],
            "status": {"1": "m"},
            "id": ["a"],
            "size": [1],
            "dimension": {}
        }"""
    jsonstat_data = json.loads(jsonstat_string)
    schemas = [schema.dataset, schema.all]
    assert validate(jsonstat_data, schemas)


def test_dataset8():
    # dataset.dimension
    jsonstat_data = {
        "version": "2.0",
        "class": "dataset",
        "value": [100, 99, 102, 103, 104],
        "status": "e",
        "dimension": {
            "metric": {"category": {}},
            "time": {"category": {}},
            "geo": {"category": {}},
            "sex": {"category": {}},
        },
        "id": ["a"],
        "size": [1]
    }
    schemas = [schema.dataset, schema.all]
    assert validate(jsonstat_data, schemas)


def test_dataset9():
    # dataset.link
    jsonstat_data = {
        "version": "2.0",
        "class": "dataset",
        "link": {
            "alternate": [
                {
                    "type": "text/csv",
                    "href": "http://provider.domain/2002/population/sex.csv"
                },
                {
                    "type": "text/html",
                    "href": "http://provider.domain/2002/population/sex.html"
                }
            ]},
        "value": [],
        "id": [],
        "size": [],
        "dimension": {}
    }
    schemas = [schema.dataset, schema.all]
    assert  validate(jsonstat_data, schemas)


def test_collection_complete():
    jsonstat_dimension_sex = {
        "label": "sex",
        "category":
            {
                "index": {"M": 0, "F": 1, "T": 2},
                "label": {
                    "M": "men",
                    "F": "women",
                    "T": "total"
                }
            }
    }

    jsonstat_dataset = {"label": "boh",
                        "dimension": {"sex": jsonstat_dimension_sex}}

    jsonstat_collection = {
        "version": "2.0",
        "class": "collection",
        "href": "http://json-stat.org/samples/oecd-canada-col.json",
        "label": "OECD-Canada Sample Collection",
        "updated": "2015-12-24",
        "link": {
            "item": [jsonstat_dataset]
        }
    }
    assert validate(jsonstat_collection, [schema.collection])
    assert jsonstat.validate(jsonstat_collection)


def test_validate():
    examples_jsonstat_org_dir = os.path.join(jsonstat._examples_dir, "www.json-stat.org")

    for filename in os.listdir(examples_jsonstat_org_dir):
        jsonstat_file = os.path.join(examples_jsonstat_org_dir, filename)
        if os.path.isfile(jsonstat_file) and jsonstat_file.endswith(".json"):
            # print("validating {}".format(jsonstat_file))
            with open(jsonstat_file) as f:
                json_string = f.read()
                try:
                    assert jsonstat.validate(json_string), "validating {}".format(jsonstat_file)
                except jsonstat.JsonStatException:
                    pass
