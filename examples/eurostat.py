# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
import os
import sys

# jsonstat
JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
try:
    import jsonstat
except ImportError:
    sys.path.append(JSONSTAT_HOME)
    import jsonstat


def test(uri, cache_dir, filename):
    pathname = os.path.join(cache_dir, filename)
    # extract collection
    collection = jsonstat.from_url(uri, pathname)
    print(collection)

    # extract dataset contained into collection
    ds = collection.dataset('nama_gdp_c')
    print(ds)
    ds.info_dimensions()

    # show some values
    v = ds.data(geo="IT", time="2011")
    print("IT gdp in 2011 was {}".format(v))


if __name__ == "__main__":
    # cache_dir directory where store json data downloaded from internet
    cache_dir = os.path.normpath(os.path.join(JSONSTAT_HOME, "tests", "fixtures", "eurostat"))
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    base = 'http://ec.europa.eu/eurostat/wdds/rest/data/v1.1/json/en/'
    uri = base + 'nama_gdp_c?precision=1&geo=IT&unit=EUR_HAB&indic_na=B1GM'
    filename = "eurostat-name_gpd_c-geo_IT.json"
    test(uri, cache_dir, filename)

    uri = base + 'nama_gdp_c?precision=1&unit=EUR_HAB&indic_na=B1GM'
    filename = "eurostat-name_gpd_c.json"
    test(uri, cache_dir, filename)

