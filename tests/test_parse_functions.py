# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import unittest
import os
from os.path import isfile, join

# jsonstat
import jsonstat


class TestParseFunctions(unittest.TestCase):
    def setUp(self):
        self.fixture_jsonstat_org_dir = os.path.join(os.path.dirname(__file__), "fixtures", "www.json-stat.org")

    def test_parse_collection(self):
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
        self.assertIsInstance(ret, jsonstat.JsonStatCollection)

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
        self.assertIsInstance(ret, jsonstat.JsonStatCollection)

    def test_parse_dataset(self):
        f = os.path.join(self.fixture_jsonstat_org_dir, "canada.json")
        dataset = jsonstat.from_file(f)
        self.assertIsNotNone(dataset)
        self.assertIsInstance(dataset, jsonstat.JsonStatDataSet)
        self.assertEqual(120, len(dataset))

    def test_parse_dimension(self):
        self.json_string_dimension = """
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
        ret = jsonstat.from_string(self.json_string_dimension)
        self.assertIsInstance(ret, jsonstat.JsonStatDimension)

    def test_parsing_json_stat_org_files(self):
        for f in os.listdir(self.fixture_jsonstat_org_dir):
            jsonstat_file = join(self.fixture_jsonstat_org_dir, f)
            if isfile(jsonstat_file) and jsonstat_file.endswith(".json"):
                # print("parsing {}".format(jsonstat_file))
                ret = jsonstat.from_file(jsonstat_file)
                msg = "parsing {}".format(jsonstat_file)
                self.assertIsNotNone(ret, msg)


if __name__ == '__main__':
    unittest.main()
