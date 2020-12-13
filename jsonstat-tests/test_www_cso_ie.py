# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2021 gf <gf@26fe.com>
# See LICENSE file

# stdlib
import os

# external lib
import pytest

# jsonstat
import jsonstat

fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "www.cso.ie")


def test_parsing_NQQ25():
    base_uri = 'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/'
    uri = base_uri + "NQQ25"
    filename = "cso_ie-NQQ25.json"

    json_string = jsonstat.download(uri, os.path.join(fixture_dir, filename))
    collection = jsonstat.JsonStatCollection()
    collection.from_string(json_string)

    # extract dataset contained into collection
    ds = collection.dataset(0)
    assert ds.dimension('Sector') is not None

    data = ds.data(0)
    assert 19960 == data.value


def test_parsing_CIA01():
    base_uri = 'http://www.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/'
    uri = base_uri + "CIA01"
    filename = "cso_ie-CIA01.json"

    json_string = jsonstat.download(uri, os.path.join(fixture_dir, filename))
    collection = jsonstat.JsonStatCollection()
    collection.from_string(json_string)

    # extract dataset contained into collection
    ds = collection.dataset(0)
    # print(ds)
    assert ds.dimension('County and Region') is not None

    data = ds.data(0)
    assert 41692 == data.value
