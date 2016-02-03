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


class TestDataSetToTable(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures")

    def test_to_table(self):
        dataset = jsonstat.JsonStatDataSet()
        json_pathname = os.path.join(self.fixture_dir, "dataset", "json_dataset_unemployment.json")
        dataset.from_file(json_pathname)
        table = dataset.to_table()

        # table len is the size of dataset + 1 for headers
        self.assertEqual(len(dataset) + 1, len(table))

        header_expected = [u'OECD countries, EU15 and total', u'2003-2014', 'Value']
        self.assertEqual(header_expected, table[0])
        first_row_expected = [u'Australia', u'2012', 11]
        self.assertEquals(first_row_expected, table[1])
        second_row_expected = [u'Austria', u'2012', 12]
        self.assertEqual(second_row_expected, table[2])

    def test_to_table_eurostat_one_dim(self):
        # convert collection to table
        collection = jsonstat.JsonStatCollection()
        json_pathname = os.path.join(self.fixture_dir, "eurostat", "eurostat-name_gpd_c-geo_IT.json")
        collection.from_file(json_pathname)
        gdp_c = collection.dataset('nama_gdp_c')
        table = gdp_c.to_table()

        # read generate table by jsonstat js module
        to_table_pathname = os.path.join(self.fixture_dir, "output_from_nodejs", "eurostat-name_gpd_c-geo_IT-to_table.csv")

        import csv
        with open(to_table_pathname, 'r') as csvfile:
            cvs_reader = csv.reader(csvfile)
            for i, row in enumerate(cvs_reader):
                msg = "table and cvs don't match at line number {}".format(i)

                def transform_row(v):
                    if v is None: return ''
                    return "{}".format(v)
                t = list(map(transform_row, table[i]))
                self.assertEquals(t, row, msg)

    @unittest.skip("working on it")
    def test_to_table_output(self):
        """
        test convert dataset to table
        """
        collection = jsonstat.JsonStatCollection()
        json_pathname = os.path.join(self.fixture_dir, "collection", "oecd-canada.json")
        collection.from_file(json_pathname)
        oecd = collection.dataset('oecd')
        table = oecd.to_table()

        # read generate table by jsonstat js module
        to_table_pathname = os.path.join(self.fixture_dir, "output_from_nodejs", "oecd-canada-to_table.csv")

        import csv
        with open(to_table_pathname, 'r') as csvfile:
            cvs_reader = csv.reader(csvfile)
            for i, row in enumerate(cvs_reader):
                # print(table[i])
                # try:
                #     row[3] = float(row[3])
                # except ValueError:
                #     pass
                # print(row)
                #
                # self.assertEquals(table[i][0], row[0])
                # self.assertEquals(table[i][1], row[1])
                # self.assertEquals(table[i][2], row[2])
                # self.assertEquals(table[i][3], row[3])

                msg = "table and cvs don't match at line number {}".format(i)
                # self.assertEquals(table[i], row, msg)
                def transform_row(v):
                    if v is None: return ''
                    return "{}".format(v)
                t = list(map(transform_row, table[i]))
                self.assertEquals(t, row, msg)






if __name__ == '__main__':
    unittest.main()
