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
import pandas.util.testing as pdt

# jsonstat
import jsonstat


class TestDataSetToTable(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures")

    #
    # to_table
    #
    def test_to_table(self):
        json_pathname = os.path.join(self.fixture_dir, "dataset", "dataset_unemployment_v1.json")
        dataset = jsonstat.JsonStatDataSet()
        dataset.from_file(json_pathname)

        table = dataset.to_table()

        # table len is the size of dataset + 1 for headers
        self.assertEqual(len(dataset) + 1, len(table))

        header_expected = [u'serie', u'2012-2014', u'OECD countries, EU15 and total', u'Value']
        self.assertEqual(header_expected, table[0])

        first_row_expected = [u'serie', u'2012', u'Australia', 11]
        self.assertEqual(first_row_expected, table[1])

        second_row_expected = [u'serie', u'2012', u'Austria', 12]
        self.assertEqual(second_row_expected, table[2])

    def test_to_table_inverted_order(self):
        json_pathname = os.path.join(self.fixture_dir, "dataset", "dataset_unemployment_v1.json")
        dataset = jsonstat.JsonStatDataSet()
        dataset.from_file(json_pathname)

        order = [i.did() for i in dataset.dimensions()]
        order = order[::-1]  # reverse list
        order = dataset._from_aidx_to_adim(order)
        table = dataset.to_table(order=order)

        # table len is the size of dataset + 1 for headers
        self.assertEqual(len(dataset) + 1, len(table))

        header_expected = ['serie', '2012-2014', 'OECD countries, EU15 and total', 'Value']
        self.assertEqual(header_expected, table[0])

        first_row_expected = ['serie', '2012', 'Australia', 11]
        self.assertEqual(first_row_expected, table[1])

        second_row_expected = ['serie', '2013', 'Australia', 21]
        self.assertEqual(second_row_expected, table[2])

    def test_to_table_eurostat_one_dim(self):
        # convert collection to table
        json_pathname = os.path.join(self.fixture_dir, "www.ec.europa.eu_eurostat", "eurostat-name_gpd_c-geo_IT.json")
        collection = jsonstat.JsonStatCollection()
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

    def test_to_table_oecd_canada(self):
        """test convert dataset to table"""
        json_pathname = os.path.join(self.fixture_dir, "www.json-stat.org", "oecd-canada.json")
        collection = jsonstat.JsonStatCollection()
        collection.from_file(json_pathname)
        oecd = collection.dataset('oecd')

        table = oecd.to_table()

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

    def test_to_table_ssb_no(self):
        """
        test convert dataset to table
        """
        json_pathname = os.path.join(self.fixture_dir, "www.ssb.no", "29843.json")
        collection = jsonstat.JsonStatCollection()
        collection.from_file(json_pathname)
        ds = collection.dataset(0)

        table = ds.to_table()

        # read generate table by jsonstat js module
        to_table_pathname = os.path.join(self.fixture_dir, "output_from_nodejs", "29843-to_table.csv")

        import csv
        with open(to_table_pathname, 'r') as csv_file:
            cvs_reader = csv.reader(csv_file)
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

    def test_to_dataframe(self):
        json_pathname = os.path.join(self.fixture_dir, "dataset", "dataset_unemployment_v1.json")
        dataset = jsonstat.JsonStatDataSet()
        dataset.from_file(json_pathname)
        df = dataset.to_table(content='id', blocked_dims={"area":"IT"}, rtype=pd.DataFrame)
        # print(df)

        ar = [['serie', '2012','IT', 14], ['serie', '2013', 'IT', 24], ['serie', '2014', 'IT', 34]]
        expected = pd.DataFrame(ar, columns=['serie', 'year','area','Value'])
        pdt.assert_frame_equal(expected, df)

        df = dataset.to_data_frame('year', content='id', blocked_dims={"area": "IT"})
        # TODO: print(df)

        ar = [['serie', 'IT', 14], ['serie', 'IT', 24], ['serie', 'IT', 34]]
        expected = pd.DataFrame(ar, columns=['serie', 'area','Value'], index=['2012','2013','2014'])
        expected.index.name = 'year'
        pdt.assert_frame_equal(expected, df)

    def test_to_data_frame_year_IT(self):
        json_pathname = os.path.join(self.fixture_dir, "dataset", "dataset_unemployment_v1.json")
        dataset = jsonstat.JsonStatDataSet()
        dataset.from_file(json_pathname)
        df = dataset.to_data_frame("year", content="id", blocked_dims={'area':"IT"})

        # print(df)
        #       serie area  Value
        # year
        # 2012  serie   IT     14
        # 2013  serie   IT     24
        # 2014  serie   IT     34

        # print(df.columns)

        # checking taht colums are ['geo','Value]
        self.assertTrue((df.columns == pd.Series(['serie', 'area','Value'])).all())
        # pdt.assert_series_equal(df.columns,pd.Series(['area', 'Value']))
        self.assertEqual(34, df.loc['2014']['Value'])


if __name__ == '__main__':
    unittest.main()
