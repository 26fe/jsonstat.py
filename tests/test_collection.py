# This file is part of jsonstat.py

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

    def test_str(self):
        collection = jsonstat.JsonStatCollection()
        collection.from_string(self.json_string_v1_one_dataset)
        out = StringIO()
        print(collection.__str__(), file=out, end="")
        expected = "dataset: 'oecd'\n"
        self.assertEquals(expected, out.getvalue())

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
