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
        pass

    def test_run_examples(self):
        JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
        examples_dir = os.path.abspath(os.path.join(JSONSTAT_HOME, "examples"))


        FNULL = open(os.devnull, 'w') # suppress output
        for f in os.listdir(examples_dir):
            example = os.path.join(examples_dir, f)
            if os.path.isfile(example) and example.endswith(".py"):
                # print(f)
                # TODO change  pythonpath env variables (?)
                # status = subprocess.call("python {}".format(example), shell=True, stdout=FNULL, stderr=FNULL)

                from subprocess import Popen, PIPE

                p = Popen(['python', example], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                # status = subprocess.call("python {}".format(example), shell=True, stdout=stdout, stderr=stderr)

                output, err = p.communicate()
                status = p.returncode
                msg = "running '{}'\nSTDOUT:\n{}\nSTDERR:\n{}".format(example, output, err)
                self.assertEquals(0, status, msg)


if __name__ == '__main__':
    unittest.main()
