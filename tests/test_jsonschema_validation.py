# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
# from __future__ import unicode_literals
import os
import unittest
import json

# external packages
from click.testing import CliRunner
import jsonschema

# jsonstat
import jsonstat


class TestJsonSchemaValidation(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures")

    def test_validate(self):

        # json_string = '{"uffa":false}'
        # json_data = json.loads(json_string)
        # print(json_data)

        jsonstat_schema_dimension = {
            "type": "object",  # dimension id
            "properties": {
                "class": {"type": "string", "enum": ["dimension"]},
                "label": {"type": "string"},
                "category": {"type": "object",
                             "properties": {"index": {"anyOf": [{"type": "array"},
                                                                {"type": "object", "properties": {
                                                                    "additionalProperties": {"type": "number"}}}
                                                                ]
                                                      },
                                            "label": {"type": "object"}
                                            },
                             }
            }
        }

        jsonstat_schema_dataset = {"type": "object",
                                   "properties": {"class": {"type": "string", "enum": ["dataset"]},
                                                  "label": {"type": "string"},
                                                  "dimension": jsonstat_schema_dimension}}

        jsonstat_schema_collection = {"type": "object",
                                      "properties": {"class": {"type": "string", "enum": ["collection"]},
                                                     "link": {"type": "object",
                                                              "properties": {"item": {"type": "array", "itmes":{"type": jsonstat_schema_dataset}}}}}
                                      }

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
            "class": "collection",
            "link": {
                "item": [jsonstat_dataset]
            }
        }

        try:
            jsonschema.validate(jsonstat_dataset, jsonstat_schema_dataset)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        try:
            jsonschema.validate(jsonstat_collection, jsonstat_schema_collection)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

if __name__ == '__main__':
    unittest.main()
