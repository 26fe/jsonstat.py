# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import os
import unittest

# jsonstat
import jsonstat


class TestWWWSsbNo(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "www.ssb.no")

    def test_one_dimension(self):
        uri = 'http://data.ssb.no/api/v0/dataset/29843.json?lang=en'

        filename = "29843.json"
        json_string = jsonstat.download(uri, os.path.join(self.fixture_dir, filename))
        collection = jsonstat.JsonStatCollection()
        collection.from_string(json_string)

        # extract dataset contained into collection
        ds = collection.dataset(0)
        # ds.info()
        # ds.dimension('PKoder').info()

        # v = ds.value(PKoder="Basic chemicals", Tid="2013M07")
        # self.assertEqual(112.2, v)

        data = ds.data(PKoder="P1111", Tid="2013M07")
        self.assertEqual(112.2, data.value)


if __name__ == '__main__':
    unittest.main()
