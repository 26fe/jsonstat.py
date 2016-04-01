# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
# from __future__ import unicode_literals
import os
import unittest

# external packages
from click.testing import CliRunner

# jsonstat
from jsonstat.cli.cli_jsonstat import cli


class TestCli(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures")

    # @unittest.skipIf(sys.version_info < (3,), "unicode issue (how sad)")
    def test_cli(self):
        # TODO: download from a local webserver, eliminate network dipendence

        cache_dir = os.path.join(self.fixture_dir, 'cli')
        args = ['info', '--cache_dir', cache_dir]
        runner = CliRunner()
        result = runner.invoke(cli, args)
        self.assertEqual(result.exit_code, 0)

        expected = [
            u"downloaded file(s) are stored into '{}'\n".format(cache_dir),
            u"download 'http://json-stat.org/samples/oecd-canada-col.json'\n",
            u"JsonstatCollection contains the following JsonStatDataSet:\n",
            u"+-----+-----------------------------------------------------+\n",
            u"| pos | dataset                                             |\n",
            u"+-----+-----------------------------------------------------+\n",
            u"| 0   | 'Unemployment rate in the OECD countries 2003-2014' |\n",
            u"| 1   | 'Population by sex and age group. Canada. 2012'     |\n",
            u"+-----+-----------------------------------------------------+\n"
        ]
        expected = ''.join(expected)
        self.maxDiff = None
        self.assertEqual(result.output, expected)


if __name__ == '__main__':
    unittest.main()
