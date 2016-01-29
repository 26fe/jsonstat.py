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


class TestEurostat(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "eurostat")

    def simple_test(self):
        base = 'http://ec.europa.eu/eurostat/wdds/rest/data/v1.1/json/en/'
        uri = base + 'nama_gdp_c?precision=1&geo=IT&unit=EUR_HAB&indic_na=B1GM'

        filename = "eurostat-name_gpd_c-geo_IT.json"
        json_string = jsonstat.download(uri, os.path.join(self.fixture_dir, filename))

        # extract collection
        collection = jsonstat.JsonStatCollection()
        collection.from_string(json_string)
        # print(collection)

        # extract dataset contained into collection
        ds = collection.dataset('nama_gdp_c')
        self.assertEquals(69, len(ds))
        time = ds.dimension('time')
        self.assertEquals(69, len(time))

        # show some values
        v = ds.value(geo="IT", time="2011")
        # print("IT gdp in 2011 was {}".format(v))
        self.assertEquals(26000, v)

        # for r in ds.to_table():
        #     print(r)


if __name__ == '__main__':
    unittest.main()
