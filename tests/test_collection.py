# This file is part of jsonstat.py

# stdlib
from __future__ import print_function
import unittest
import os
# jsonstat
import jsonstat
from jsonstat.collection import JsonStatCollection


class TestCollection(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "collection")

        self.json_string_v1 = """
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

    def test_parse_v1(self):
        collection = JsonStatCollection()
        collection.from_string(self.json_string_v1)
        self.assertIsNotNone(collection.dataset('oecd'))
        self.assertIsNotNone(collection.dataset('canada'))

    def test_parse_v2(self):
        collection = JsonStatCollection()
        filename = os.path.join(self.fixture_dir, "oecd-canada-col.json")
        collection.from_file(filename)
        oecd = collection.dataset(0)
        self.assertIsNotNone(oecd)
        canada = collection.dataset(1)
        self.assertIsNotNone(canada)


if __name__ == '__main__':
    unittest.main()
