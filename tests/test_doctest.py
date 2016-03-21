# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import unittest
import doctest

import jsonstat.dimension


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(jsonstat.dimension))
    return tests


if __name__ == '__main__':
    unittest.main()
