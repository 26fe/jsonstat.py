# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import sys
import unittest
import doctest

# jsonstat
import jsonstat.dimension


def load_tests(loader, tests, ignore):
    # add doctest only if python version is 3 or better
    if sys.version_info >= (3,):
        doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
        tests.addTests(doctest.DocTestSuite(jsonstat.parse_functions))
        tests.addTests(doctest.DocTestSuite(jsonstat.dimension))
        tests.addTests(doctest.DocTestSuite(jsonstat.dataset))
        tests.addTests(doctest.DocTestSuite(jsonstat.collection))
    return tests


if __name__ == '__main__':
    unittest.main()
