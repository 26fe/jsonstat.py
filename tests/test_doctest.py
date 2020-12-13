# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2021 gf <gf@26fe.com>
# See LICENSE file

# stdlib
import sys
import os
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
        doc_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
        tests.addTests(doctest.DocFileSuite(os.path.join(doc_dir, 'tutorial.rst'), module_relative=False))
    return tests


if __name__ == '__main__':
    unittest.main()
