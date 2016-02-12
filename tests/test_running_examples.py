# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import subprocess
import os
import unittest

import sys
# TODO: remove following hack
# http://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
if sys.version_info < (3,):
    reload(sys)
    sys.setdefaultencoding('utf8')

class TestRunningExamples(unittest.TestCase):
    def setUp(self):
        JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
        self.examples_dir = os.path.abspath(os.path.join(JSONSTAT_HOME, "examples"))

    # @unittest.skip("working on it")
    def test_run_examples(self):
        for example in os.listdir(self.examples_dir):
            example_path = os.path.join(self.examples_dir, example)
            if os.path.isfile(example_path) and example_path.endswith(".py"):
                self.__run_file(example)

    # @unittest.skip("disabled")
    # def test_eurostat(self):
    #     self.__run_file("eurostat.py")

    def __run_file(self, example):
        example_path = os.path.join(self.examples_dir, example)
        # FNULL = open(os.devnull, 'w') # suppress output
        # print(f)
        # TODO change  pythonpath env variables (?)
        # status = subprocess.call("python {}".format(example), shell=True, stdout=FNULL, stderr=FNULL)
        from subprocess import Popen, PIPE
        p = Popen(['python', example_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        # status = subprocess.call("python {}".format(example), shell=True, stdout=stdout, stderr=stderr)
        output, err = p.communicate()
        status = p.returncode
        msg = "running '{}'\nSTDOUT:\n{}\nSTDERR:\n{}".format(example, output, err)
        self.assertEqual(0, status, msg)

if __name__ == '__main__':
    unittest.main()
