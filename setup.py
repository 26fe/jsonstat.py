# stdlib
import os
import re
from setuptools import setup


# version_file = open(os.path.join(mypackage_root_dir, 'VERSION'))
# version = version_file.read().strip()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


exec(open('jsonstat/version.py').read())


# cannot be able to import only version
# because import jsonstat.version execute __init__
# and not all dependencies are in place
# from jsonstat.version import __version__

# with open('requirements.txt') as f:
#     install_requires = f.read().splitlines()
#
# with open('requirements_for_test.txt') as f:
#     tests_require = f.read().splitlines()


# From cburgmer/pdfserver
# https://github.com/cburgmer/pdfserver/blob/master/setup.py
def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            # TODO support version numbers
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements


def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links


# execfile is only python 2
# execfile('jsonstat/version.py')

# if sys.version_info >= (3,2):
#     install_requires = ["threadpool >= 1.2.7"]
# else:
#     install_requires = ["threadpool >= 1.2.3"]

setup(
    name="jsonstat.py",
    description='Library for reading JSON-stat format data.',
    long_description=read('README.rst'),
    keywords="jsonstat jsonstats json statistics",

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Environment :: Console',

        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],

    version=__version__,
    url='https://github.com/26fe/jsonstat.py',

    author='26fe',
    author_email='gf@26fe.com',

    license='LGPL',

    # packages= setup.find_packages(exclude=['examples', 'docs', 'tests*', 'tmp']),
    packages=[
        'jsonstat', 'jsonstat.cli', 'istat'
    ],

    package_data={
        'jsonstat': [
            'schema/collection.json',
            'schema/dataset.json',
            'schema/dimension.json',
            'schema/jsonstat.json',
        ],
    },

    data_files=[('', ['requirements.txt'])],
    include_package_data=True,

    install_requires=parse_requirements('requirements.txt'),
    dependency_links=parse_dependency_links('requirements.txt'),
    tests_require=parse_requirements('requirements_for_test.txt'),

    entry_points={
        'console_scripts': [
            'jsonstat=jsonstat.cli.cli_jsonstat:cli',  # command=package.module:function
        ],
    },

)
