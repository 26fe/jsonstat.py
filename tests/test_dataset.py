# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import unittest
import os

# jsonstat
import jsonstat


class TestDataSet(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "dataset")

        self.json_missing_value = '''
        {
		    "label" : "three dimensions"
		}
		'''

        self.json_missing_dimension = '''
        {
		    "label" : "three dimensions",
		    "value" : []
		}
		'''

        self.json_string_incorrect_data_size = '''
        {
		    "label" : "Unemployment rate in the OECD countries 2003-2014",
		    "source" : "Economic Outlook No 92 - December 2012 - OECD Annual Projections",
		    "value" : [1, 2, 3, 4],
		    "dimension" : {
		        "id" : ["area", "year"],
		        "size" : [4, 12],
		        "area" : {
		            "category" : { "index" : { "AU" : 0, "AT" : 1, "BE" : 2, "CA" : 3 } }
                },
                "year" : {
                    "category" : {
                        "index" : {
                            "2003" : 0, "2004" : 1, "2005" : 2, "2006" : 3, "2007" : 4,
                            "2008" : 5, "2009" : 6,
                            "2010" : 7, "2011" : 8, "2012" : 9, "2013" : 10, "2014" : 11
                        }
                    }
		        }
		    }
		}
		'''

    def test_exception_not_valid(self):
        dataset = jsonstat.JsonStatDataSet("canada")
        with self.assertRaises(jsonstat.JsonStatException):
            dataset.value(year="2003", area="CA")

    def test_missing_value_field(self):
        dataset = jsonstat.JsonStatDataSet("canada")
        with self.assertRaises(jsonstat.JsonStatMalformedJson) as cm:
            dataset.from_string(self.json_missing_value)
        e = cm.exception
        expected = "dataset 'canada': missing 'value' key"
        self.assertEqual(expected, e.value)

    def test_missing_dimension(self):
        dataset = jsonstat.JsonStatDataSet("canada")
        with self.assertRaises(jsonstat.JsonStatMalformedJson) as cm:
            dataset.from_string(self.json_missing_dimension)
        e = cm.exception
        expected = "dataset 'canada': missing 'dimension' key"
        self.assertEqual(expected, e.value)

    def test_exception_dataset_size(self):
        dataset = jsonstat.JsonStatDataSet("canada")
        with self.assertRaises(jsonstat.JsonStatException) as cm:
            dataset.from_string(self.json_string_incorrect_data_size)
        e = cm.exception
        # expected e il primo valore dell'assert (giusto per ricordare!)
        expected = "dataset 'canada': size 4 is different from calculate size 48 by dimension"
        self.assertEqual(expected, e.value)

    def test_name(self):
        dataset = jsonstat.JsonStatDataSet("canada")
        self.assertEquals(dataset.name(), "canada")

    def test_dimensions(self):
        dataset = jsonstat.JsonStatDataSet("canada")
        dataset.from_file(os.path.join(self.fixture_dir, "json_dataset_unemployment.json"))
        self.assertEquals(len(dataset.dimensions()), 2)

    def test_get_dim(self):
        dataset = jsonstat.JsonStatDataSet("canada")
        dataset.from_file(os.path.join(self.fixture_dir, "json_dataset_unemployment.json"))
        self.assertEquals(dataset.dimension("year").name(), "year")
        with self.assertRaises(KeyError):
            dataset.dimension("not existent dim")

    def test_info(self):
        dataset = jsonstat.JsonStatDataSet("canada")
        dataset.from_file(os.path.join(self.fixture_dir, "json_dataset_unemployment.json"))

        expected =(
            "name:   'canada'\n"
            "label:  'Unemployment rate in the OECD countries'\n"
            "source: 'Unemployment rate in the OECD countries'\n"
            "size: 12\n"
            "2 dimensions:\n"
            "  0: dim id/name: 'area' size: '4' role: 'geo'\n"
            "  1: dim id/name: 'year' size: '3' role: 'time'\n"
        )
        self.assertEquals(expected, dataset.__str__())

    def test_value(self):
        dataset = jsonstat.JsonStatDataSet("canada")
        dataset.from_file(os.path.join(self.fixture_dir, "json_dataset_unemployment.json"))
        self.assertEquals(dataset.value(area="AU", year="2012"), 11)
        self.assertEquals(dataset.value(area="BE", year="2014"), 33)

    def test_all_pos(self):
        dataset = jsonstat.JsonStatDataSet("canada")
        dataset.from_file(os.path.join(self.fixture_dir, "json_dataset_unemployment.json"))
        result = list(dataset.all_pos())
        expected = [[0, 0], [1, 0], [2, 0], [3, 0], [0, 1], [1, 1], [2, 1], [3, 1], [0, 2], [1, 2], [2, 2], [3, 2]]
        self.assertEquals(result, expected)

    def test_all_pos_with_block(self):
        dataset = jsonstat.JsonStatDataSet("canada")
        dataset.from_file(os.path.join(self.fixture_dir, "json_dataset_unemployment.json"))

        result = list(dataset.all_pos({"area":"IT"}))
        expected = [[3, 0], [3, 1], [3, 2]]
        self.assertEquals(result, expected)

        dataset.generate_all_vec(area="IT")

        result = list(dataset.all_pos({"year":"2014"}))
        expected = [[0, 2], [1, 2], [2, 2], [3, 2]]
        self.assertEquals(result, expected)

        dataset.generate_all_vec(year='2014')

    def test_all_pos_with_three_dim(self):
        dataset = jsonstat.JsonStatDataSet()
        dataset.from_file(os.path.join(self.fixture_dir, "json_three_dimensions.json"))

        result = list(dataset.all_pos({'one':'one_1'}))

        expected = [
            [0, 0, 0],[0, 1, 0],[0, 2, 0],[0, 0, 1],
            [0, 1, 1],[0, 2, 1],[0, 0, 2],[0, 1, 2],
            [0, 2, 2],[0, 0, 3],[0, 1, 3],[0, 2, 3]
        ]

        self.assertEquals(result, expected)
        dataset.generate_all_vec(one='one_1')

        result = list(dataset.all_pos({"two":"two_2"}))
        expected = [
            [0, 1, 0],[1, 1, 0],[0, 1, 1],[1, 1, 1],[0, 1, 2],[1, 1, 2],[0, 1, 3],[1, 1, 3]
        ]
        self.assertEquals(result, expected)

    def test_to_data_frame_year_IT(self):
        dataset = jsonstat.JsonStatDataSet()
        dataset.from_file(os.path.join(self.fixture_dir, "json_dataset_unemployment.json"))
        df = dataset.to_data_frame("year", area="IT")

        # print df
        self.assertEquals(df['IT']['2014'], 34)

    # def test_extract_year_all_country(self):
    #     dataset = jsonstat.JsonStatSingleDataSet("canada")
    #     dataset.from_string(self.json_dataset_unemployment)
    #     df = dataset.to_data_frame("year")
    #
    #     # print df
    #     self.assertEquals(df['IT']['2014'], 34)


if __name__ == '__main__':
    unittest.main()
