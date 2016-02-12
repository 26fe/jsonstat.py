# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import unittest
import os

# external packages
import pandas as pd

# jsonstat
import jsonstat


class TestDataSetToTable(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures")

    #
    # to_table
    #
    def test_to_table(self):
        dataset = jsonstat.JsonStatDataSet()
        json_pathname = os.path.join(self.fixture_dir, "dataset", "json_dataset_unemployment.json")
        dataset.from_file(json_pathname)
        table = dataset.to_table()

        # table len is the size of dataset + 1 for headers
        self.assertEqual(len(dataset) + 1, len(table))

        header_expected = [u'2003-2014', u'OECD countries, EU15 and total', u'Value']
        self.assertEqual(header_expected, table[0])
        first_row_expected = [u'2012', u'Australia', 11]
        self.assertEqual(first_row_expected, table[1])
        second_row_expected = [u'2013', u'Australia', 21]
        self.assertEqual(second_row_expected, table[2])

        df = dataset.to_table(content='id', blocked_dims={"area":"IT"}, rtype=pd.DataFrame)
        # TODO: print(df)

        df = dataset.to_data_frame('year', content='id', blocked_dims={"area":"IT"})
        # TODO: print(df)

    def test_to_table_inverted_order(self):
        dataset = jsonstat.JsonStatDataSet()
        json_pathname = os.path.join(self.fixture_dir, "dataset", "json_dataset_unemployment.json")
        dataset.from_file(json_pathname)
        order = [i.name() for i in dataset.dimensions()]
        order = order[::-1]  # reverse list
        order = dataset.from_vec_idx_to_vec_dim(order)
        table = dataset.to_table(order=order)

        # table len is the size of dataset + 1 for headers
        self.assertEqual(len(dataset) + 1, len(table))

        header_expected = ['2003-2014', 'OECD countries, EU15 and total', 'Value']
        self.assertEqual(header_expected, table[0])
        first_row_expected = ['2012', 'Australia', 11]
        self.assertEqual(first_row_expected, table[1])
        second_row_expected = ['2012', 'Austria', 12]
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
                self.assertEqual(t, row, msg)

    def test_to_table_output(self):
        """
        test convert dataset to table
        """
        collection = jsonstat.JsonStatCollection()
        json_pathname = os.path.join(self.fixture_dir, "collection", "oecd-canada.json")
        collection.from_file(json_pathname)
        oecd = collection.dataset('oecd')

        order = [i.name() for i in oecd.dimensions()]
        order = order[::-1]  # reverse list
        order = oecd.from_vec_idx_to_vec_dim(order)
        table = oecd.to_table(order=order)

        # read generate table by jsonstat js module
        to_table_pathname = os.path.join(self.fixture_dir, "output_from_nodejs", "oecd-canada-to_table.csv")

        import csv
        with open(to_table_pathname, 'r') as csvfile:
            cvs_reader = csv.reader(csvfile)
            for i, row in enumerate(cvs_reader):
                msg = "table and cvs don't match at line number {}".format(i)
                def transform_row(v):
                    if v is None: return ''
                    return "{}".format(v)
                t = list(map(transform_row, table[i]))
                self.assertEqual(t, row, msg)

    #
    # to_data_frame
    #
    @unittest.skip("working on it")
    def test_to_data_frame_year_IT(self):
        dataset = jsonstat.JsonStatDataSet()
        dataset.from_file(os.path.join(self.fixture_dir, "dataset", "json_dataset_unemployment.json"))
        df = dataset.to_data_frame("year", content="id", blocked_dims={'area':"IT"})

        # print(df)
        self.assertEqual(df['IT'], 34)


if __name__ == '__main__':
    unittest.main()
