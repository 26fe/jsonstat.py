# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
# from __future__ import unicode_literals
import sys
import unittest

# external packages
from click.testing import CliRunner

# jsonstat
from jsonstat.cli.cli_jsonstat import jsonstat_cli


class TestCollection(unittest.TestCase):
    def setUp(self):
        pass

    # @unittest.skipIf(sys.version_info < (3,), "unicode issue (how sad)")
    def test_cli(self):
        # TODO: download from a local webserver, eliminate network dipendence
        runner = CliRunner()
        result = runner.invoke(jsonstat_cli)
        self.assertEqual(result.exit_code, 0)

        # print("#{}#".format(result.output))
        expected = (
            u"downloaded file(s) are stored into './data'\n"
            u"download 'http://json-stat.org/samples/oecd-canada.json'\n"
            u"JsonstatCollection contains the following JsonStatDataSet:\n"
            u"0: dataset 'oecd'\n"
            u"1: dataset 'canada'\n\n"
        )
        self.assertEqual(result.output, expected)
