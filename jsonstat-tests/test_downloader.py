# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2021 gf <gf@26fe.com>
# See LICENSE file

# stdlib

# external modules
import pytest
import requests
import requests_mock

# jsonstat
import jsonstat.downloader
import jsonstat


def test_downloader(tmpdir):
    # tmpdir is a LocalPath type in 3.6
    # it must be converted it in str for < 3.6
    uri = 'http://json-stat.org/samples/oecd-canada.json'
    body = 'This is a test'

    with requests_mock.mock() as m:
        m.get(uri, text=body)
        d = jsonstat.Downloader(cache_dir=str(tmpdir))
        response = d.download(uri)

    assert body == response


def test_downloader_with_no_cache_dir():
    uri = 'http://json-stat.org/samples/oecd-canada.json'
    body = 'This is a test'

    with requests_mock.mock() as m:
        m.get(uri, text=body)
        d = jsonstat.Downloader(cache_dir=None)
        response = d.download(uri)

    assert body == response
