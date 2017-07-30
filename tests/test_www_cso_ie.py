# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2017 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import os
import unittest

# jsonstat
import jsonstat


class TestWWWCsoIe(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "www.cso.ie")

    def test_parsing_NQQ25(self):
        base_uri = 'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/'
        uri = base_uri + "NQQ25"
        filename = "cso_ie-NQQ25.json"

        json_string = jsonstat.download(uri, os.path.join(self.fixture_dir, filename))
        collection = jsonstat.JsonStatCollection()
        collection.from_string(json_string)

        # extract dataset contained into collection
        ds = collection.dataset(0)
        self.assertIsNotNone(ds.dimension('Sector'))

        data = ds.data(0)
        self.assertEqual(19960, data.value)

    def test_parsing_CIA01(self):
        base_uri = 'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/'
        uri = base_uri + "CIA01"
        filename = "cso_ie-CIA01.json"

        json_string = jsonstat.download(uri, os.path.join(self.fixture_dir, filename))
        collection = jsonstat.JsonStatCollection()
        collection.from_string(json_string)

        # extract dataset contained into collection
        ds = collection.dataset(0)
        # print(ds)
        self.assertIsNotNone(ds.dimension('County and Region'))

        data = ds.data(0)
        self.assertEqual(41692, data.value)


if __name__ == '__main__':
    unittest.main()
