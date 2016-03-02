# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import os
import unittest

# external modules
import requests

# test modules
from sure import expect
import httpretty

# jsonstat
import jsonstat
import jsonstat.downloader


class TestDownloader(unittest.TestCase):

    def setUp(self):
        JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
        self.__temp_dir = os.path.join(JSONSTAT_HOME, "tmp")

    @httpretty.activate
    def test_downloader(self):
        uri = 'http://json-stat.org/samples/oecd-canada.json'
        json_filename = "oecd-canada.json"
        body = 'This is a test'
        httpretty.register_uri(
            httpretty.GET, uri,
            body=body,
            content_type="application/json")

        d = jsonstat.Downloader(cache_dir=self.__temp_dir)
        response = d.download(uri)

        self.assertEqual(body, response)

        # expect(response.json()).to.equal([{"title": "test"}])


if __name__ == '__main__':
    unittest.main()
