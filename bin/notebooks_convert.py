# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2017 gf <gf@26fe.com>
# See LICENSE file

# stdlib
import os
import shutil
from subprocess import Popen, PIPE


def convert_notebook_to_rst(dir):
    print("***** {}".format(dir))
    for f in os.listdir(dir):
        # print(f)
        notebook_path = os.path.join(dir, f)
        if os.path.isfile(notebook_path) and notebook_path.endswith(".ipynb"):
            # print("converting {}".format(notebook_path))

            notebook_name = os.path.splitext(f)[0]
            lst = ['jupyter', 'nbconvert', '--to=rst', '--output', notebook_name, notebook_path]
            cmd = " ".join(lst)
            print(cmd)
            p = Popen(lst, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate()
            status = p.returncode
            if status != 0:
                print("ERROR!")
                print(err)


if __name__ == "__main__":
    JSONSTAT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    docs_notebooks = os.path.join(JSONSTAT_HOME, "docs", "notebooks")

    print("remove output directory")
    shutil.rmtree(docs_notebooks)

    if not os.path.exists(docs_notebooks):
        os.mkdir(docs_notebooks)

    os.chdir(docs_notebooks)
    dirs = ["examples-notebooks", "istat-notebooks"]
    for d in dirs:
        dd = os.path.join(JSONSTAT_HOME, d)
        convert_notebook_to_rst(dd)
