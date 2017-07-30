# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2017 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals

import os
import unittest

# jsonstat/istat
import jsonstat
import istat


class TestIstat(unittest.TestCase):

    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "istat")

    def test_cache_dir(self):
        istat.cache_dir('/tmp')
        cd = istat.cache_dir()
        self.assertEqual(cd, '/tmp')

    def test_options(self):
        self.assertEqual(3, istat.options.display.max_rows)

if __name__ == '__main__':
    unittest.main()
