# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import sys
import unittest

# jsonstat
import jsonstat


class TestDimension(unittest.TestCase):

    def setUp(self):
        self.json_str_only_index= '''
        {
            "label" : "2003-2014",
            "category" : {
                "index" : {
                    "2003" : 0,
                    "2004" : 1,
                    "2005" : 2,
                    "2006" : 3,
                    "2007" : 4,
                    "2008" : 5,
                    "2009" : 6,
                    "2010" : 7,
                    "2011" : 8,
                    "2012" : 9,
                    "2013" : 10,
                    "2014" : 11
                }
            }
        }
        '''

        self.json_str_hole_in_index= '''
        {
            "label" : "2003-2014",
            "category" : {
                "index" : {
                    "2003" : 0,
                    "2004" : 1,
                    "2005" : 2,
                    "2006" : 3,
                    "2011" : 8,
                    "2012" : 9,
                    "2013" : 10,
                    "2014" : 11
                }
            }
        }
        '''

        self.json_str_size_one= '''
            {
                "label" : "country",
                "category" : {"label" : { "CA" : "Canada" }}
            }
        '''


        self.json_str_label_and_index= '''
            {
                "label" : "OECD countries, EU15 and total",
                "category" : {
                    "index" : { "AU" : 0, "AT" : 1, "BE" : 2, "IT": 3 },
                    "label" : { "AU" : "Australia", "AT" : "Austria", "BE" : "Belgium", "CA" : "Canada", "IT":"Italy" }
                }
            }
        '''

    def test_getters(self):
        dim = jsonstat.JsonStatDimension("test_dim", 10, 0, 'role')
        self.assertEqual(dim.name(), "test_dim")
        self.assertEqual(dim.size(), 10)
        self.assertEqual(dim.pos(), 0)
        self.assertEqual(dim.role(), "role")

    def test_exception_not_valid(self):
        dim = jsonstat.JsonStatDimension("year", 10, 0, None)
        with self.assertRaises(jsonstat.JsonStatException):
            r = dim.idx2pos('2013')

    def test_exception_size(self):
        dim = jsonstat.JsonStatDimension("year", 10, 0, None)

        with self.assertRaises(jsonstat.JsonStatException):
            dim.from_string(self.json_str_only_index)

    def test_exception_hole_in_category_index(self):
        dim = jsonstat.JsonStatDimension("year", 8, 0, None)

        r = "index \d+ for dimension 'year' is greater than size 8"

        # following code doesn't work with python 2.7.11
        # with self.assertRaisesRegex(jsonstat.JsonStatException, r):
        #     dim.from_string(self.json_string_hole_in_index)

        with self.assertRaises(jsonstat.JsonStatException) as cm:
            dim.from_string(self.json_str_hole_in_index)
        e = cm.exception
        if sys.version_info < (3,):
            self.assertRegexpMatches(e.value, r)
        else:
            self.assertRegex(e.value, r)

    def test_size_one(self):
        dim = jsonstat.JsonStatDimension("country", 1, 0, None)
        dim.from_string(self.json_str_size_one)
        self.assertEqual(u'country', dim.label())
        self.assertEqual(1, len(dim))

    def test_idx2pos(self):
        dim = jsonstat.JsonStatDimension("year", 12, 0, None)
        dim.from_string(self.json_str_only_index)
        self.assertEqual(dim.idx2pos("2003"), 0)
        self.assertEqual(dim.idx2pos("2014"), 11)

    def test_pos2idx(self):
        dim = jsonstat.JsonStatDimension("year", 12, 0, None)
        dim.from_string(self.json_str_only_index)
        self.assertEqual(dim.pos2idx(0), "2003")
        self.assertEqual(dim.pos2idx(11), "2014")

    def test_get_index(self):
        dim = jsonstat.JsonStatDimension("year", 12, 0, None)
        dim.from_string(self.json_str_only_index)
        expected = ['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014']
        result = dim.get_index()
        self.assertEqual(expected, result)

    def test_info(self):
        dim = jsonstat.JsonStatDimension("year", 12, 0, None)
        dim.from_string(self.json_str_only_index)
        expected = (
            "index\n"
            "  pos    idx  label\n"
            "    0   2003       \n"
            "    1   2004       \n"
            "    2   2005       \n"
            "    3   2006       \n"
            "    4   2007       \n"
            "    5   2008       \n"
            "    6   2009       \n"
            "    7   2010       \n"
            "    8   2011       \n"
            "    9   2012       \n"
            "   10   2013       \n"
            "   11   2014       \n"
        )
        self.maxDiff = None
        self.assertEqual(expected, dim.__str__())

    def test_info_with_label(self):
        dim = jsonstat.JsonStatDimension("concept", 1, 0, None)
        dim.from_string(self.json_str_size_one)
        expected = (
            "index\n"
            "  pos    idx  label\n"
            "    0     CA Canada\n"
        )
        self.maxDiff = None
        self.assertEqual(expected, dim.__str__())

    def test_exception_mismatch_index_and_label(self):
        dim = jsonstat.JsonStatDimension("year", 4, 0, None)
        with self.assertRaises(jsonstat.JsonStatMalformedJson) as cm:
            dim.from_string(self.json_str_label_and_index)

        e = cm.exception
        expected = "dimension 'year': label 'Canada' is associated with index 'CA' that not exists!"
        self.assertEqual(e.value, expected)

if __name__ == '__main__':
    unittest.main()
