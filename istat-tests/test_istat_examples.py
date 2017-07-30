# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2017 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import os
import sys
from subprocess import Popen, PIPE
import unittest

# python 2.7.11 raise the following error
#    UnicodeEncodeError: 'ascii' codec can't encode character u'\x96' in position 17: ordinal not in range(128)
# to prevent it the following three lines are added:
# See: http://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
if sys.version_info < (3,):
    reload(sys)
    sys.setdefaultencoding('utf8')


class TestIstatExamples(unittest.TestCase):
    def setUp(self):
        JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
        self.examples_dir = os.path.abspath(os.path.join(JSONSTAT_HOME, "istat-examples"))

    @unittest.skipIf(os.environ.get("TRAVIS"), "skipped on travis")
    def test_run_examples(self):
        for example in os.listdir(self.examples_dir):
            example_path = os.path.join(self.examples_dir, example)
            if os.path.isfile(example_path) and example_path.endswith(".py"):
                self.__run_file(example)

    def __run_file(self, example):
        example_path = os.path.join(self.examples_dir, example)
        p = Popen(['python', example_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        status = p.returncode
        msg = "running '{}'\nSTDOUT:\n{}\nSTDERR:\n{}".format(example, output, err)
        self.assertEqual(0, status, msg)


if __name__ == '__main__':
    unittest.main()
