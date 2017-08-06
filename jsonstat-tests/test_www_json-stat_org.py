# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2017 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import os
from os.path import isfile, join

# external modules
import pytest

# jsonstat
import jsonstat

fixture_jsonstat_org_dir = os.path.join(jsonstat._examples_dir, "www.json-stat.org")


def test_parsing_json_stat_org_files():
    for f in os.listdir(fixture_jsonstat_org_dir):
        jsonstat_file = join(fixture_jsonstat_org_dir, f)
        if isfile(jsonstat_file) and jsonstat_file.endswith(".json"):
            # print("parsing {}".format(jsonstat_file))
            ret = jsonstat.from_file(jsonstat_file)
            msg = "parsing {}".format(jsonstat_file)
            assert ret is not None, msg
