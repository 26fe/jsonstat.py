
import os
from subprocess import Popen, PIPE


def run_all_notebooks(dir):
    print("***** {}".format(dir))
    for f in os.listdir(dir):
        # print(f)
        notebook_path = os.path.join(dir, f)
        if os.path.isfile(notebook_path) and notebook_path.endswith(".ipynb"):
            print("running {}".format(notebook_path))
            p = Popen(['runipy', notebook_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate()
            status = p.returncode
            if status != 0:
                print("ERROR!")

# jupyter nbconvert --to=rst --ExecutePreprocessor.enabled=True eurostat.ipynb

JSONSTAT_HOME = os.path.normpath(os.path.join(os.path.dirname(__file__)))
dirs = ["examples-notebooks", "istat-notebooks"]
for d in dirs:
    dd = os.path.join(JSONSTAT_HOME, d)
    run_all_notebooks(dd)