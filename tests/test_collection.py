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


class TestCollection(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "collection")

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

    def test_one_dataset_to_str(self):
        collection = jsonstat.JsonStatCollection()
        collection.from_string(self.json_string_v1_one_dataset)
        out = StringIO()
        print(collection.__str__(), file=out, end="")
        expected = "0: dataset 'oecd'\n"
        self.assertEqual(expected, out.getvalue())

    def test_two_datasets_to_str(self):
        collection = jsonstat.JsonStatCollection()
        collection.from_string(self.json_string_v1_two_datasets)
        out = StringIO()
        print(collection.__str__(), file=out, end="")
        expected = "0: dataset 'oecd'\n1: dataset 'canada'\n"
        self.assertEqual(expected, out.getvalue())

    def test_parse_v1_from_string(self):
        collection = jsonstat.JsonStatCollection()
        collection.from_string(self.json_string_v1_two_datasets)

        self.assertIsNotNone(collection.dataset('oecd'))
        self.assertIsNotNone(collection.dataset('canada'))

    def test_parse_v1_from_file(self):
        filename = os.path.join(self.fixture_dir, "oecd-canada.json")
        collection = jsonstat.JsonStatCollection()
        collection.from_file(filename)

        self.assertIsNotNone(collection.dataset('oecd'))
        self.assertIsNotNone(collection.dataset('canada'))

        oecd = collection.dataset("oecd")
        dim = oecd.dimension("concept")
        expected = (
            "index\n"
            "  pos idx      label   \n"
            "    0 'UNR'    'unemployment rate'\n"
        )
        self.assertEqual(expected, dim.__str__())

    def test_parse_v2_from_file(self):
        filename = os.path.join(self.fixture_dir, "oecd-canada-col.json")
        collection = jsonstat.JsonStatCollection()
        collection.from_file(filename)

        oecd = collection.dataset(0)
        self.assertIsNotNone(oecd)

        canada = collection.dataset(1)
        self.assertIsNotNone(canada)


if __name__ == '__main__':
    unittest.main()
