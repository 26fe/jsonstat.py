# stdlib
import sys
import os
from setuptools import setup

# version_file = open(os.path.join(mypackage_root_dir, 'VERSION'))
# version = version_file.read().strip()


# if sys.version_info >= (3,2):
#     install_requires = ["threadpool >= 1.2.7"]
# else:
#     install_requires = ["threadpool >= 1.2.3"]
#
# setup(..., install_requires=install_requires)

# execfile('jsonstat/version.py')

__version__ = "0.1.0"



# from https://pythonhosted.org/an_example_pypi_project/setuptools.html
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now
# 1) we have a top level README file and
# 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
      name = "jsonstat.py",
      description = ("jsonstat.py  is a python library for reading **JSON-stat** format data."),
      long_description=read('README.rst'),
      keywords = "jsonstat json statistics",


      classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "Topic :: Software Development :: Libraries",

        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
      ],

      version=__version__,
      url='https://github.com/26fe/jsonstat.py',

      author='26fe',
      author_email='git@26fe.com',

      license='LGPL',
      # packages= setup.find_packages(exclude=['examples', 'docs', 'tests*', 'tmp']),
      packages=[
          'jsonstat',
      ],

      install_requires=[
          'pandas', 'ijson', 'requests'
      ],
      )

