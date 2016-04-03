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
    print("downloading data from '{}'".format(uri))
    collection = jsonstat.from_url(uri, pathname)
    print(collection)

    # extract dataset contained into collection
    ds = collection.dataset(0)
    print(ds)
    ds.info_dimensions()

    # show some values
    v = ds.data(0)
    lcat = ds.idx_as_lcat(0)
    print("{} -> {}".format(lcat, v.value))


if __name__ == "__main__":
    # cache_dir directory where store json data downloaded from internet
    cache_dir = os.path.normpath(os.path.join(JSONSTAT_HOME, "tests", "fixtures", "www.cso.ie"))
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    base_uri = 'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/'
    uri = base_uri + "NQQ25"
    filename = "cso_ie-NQQ25.json"
    test(uri, cache_dir, filename)

    uri = base_uri + 'CIA01'
    filename = "cso_ie-CIA01.json"
    test(uri, cache_dir, filename)
