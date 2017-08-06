# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2017 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals

import os
import unittest

# external modules
import pytest

# jsonstat/istat
import istat


fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "istat")


def test_cache_dir(tmpdir):
    istat.cache_dir(str(tmpdir))
    cd = istat.cache_dir()
    assert cd == str(tmpdir)


def test_options():
    assert 3 == istat.options.display.max_rows
