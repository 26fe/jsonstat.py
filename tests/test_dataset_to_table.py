# This file is part of jsonstat.py

# stdlib
from __future__ import print_function
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

    @unittest.skip("working on it")
    def test_to_table_output(self):
        collection = jsonstat.JsonStatCollection()
        json_pathname = os.path.join(self.fixture_dir, "collection", "oecd-canada.json")
        collection.from_file(json_pathname)
        oecd = collection.dataset('oecd')
        table = oecd.to_table()

        to_table_pathname = os.path.join(self.fixture_dir, "output_from_nodejs", "oecd-canada-to_table.csv")

        import csv
        with open(to_table_pathname, 'r') as csvfile:
            cvs_reader = csv.reader(csvfile)
            for i, row in enumerate(cvs_reader):
                print(table[i])
                print(row)
                self.assertEquals(table[i], row, "line number {}".format(i))


if __name__ == '__main__':
    unittest.main()
