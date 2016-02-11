# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import unittest
import os
from io import StringIO

# jsonstat
import jsonstat


class TestFactory(unittest.TestCase):
    def setUp(self):
        self.fixture_jsonstat_org_dir = os.path.join(os.path.dirname(__file__), "fixtures", "json-stat.org")

        self.json_string_v1_one_dataset = """
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

        self.json_string_v1_two_datasets = """
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

    def test_parse_collection(self):
        ret = jsonstat.from_string(self.json_string_v1_one_dataset)
        self.assertIsInstance(ret, jsonstat.JsonStatCollection)

    def test_parse_dataset(self):
        f = os.path.join(self.fixture_jsonstat_org_dir, "canada.json")
        dataset = jsonstat.from_file(f)
        self.assertIsNotNone(dataset)
        self.assertIsInstance(dataset, jsonstat.JsonStatDataSet)
        self.assertEquals(120, len(dataset))

    def test_dimension(self):
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

    def test_json_stat_org(self):

        from os import listdir
        from os.path import isfile, join
        onlyfiles = [f for f in listdir(self.fixture_jsonstat_org_dir) if isfile(join(self.fixture_jsonstat_org_dir, f))]
        # print(onlyfiles)
        for f in onlyfiles:
            # print("parsing {}".format(f))
            ret = jsonstat.from_file(os.path.join(self.fixture_jsonstat_org_dir, f))
            self.assertIsNotNone(ret)


if __name__ == '__main__':
    unittest.main()
