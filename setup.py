# stdlib
import os
import re
from setuptools import setup
import re
import sys, io


# version_file = open(os.path.join(mypackage_root_dir, 'VERSION'))
# version = version_file.read().strip()

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


exec(open('jsonstat/version.py').read())


# cannot be able to import only version
# because import jsonstat.version execute __init__
# and not all dependencies are in place
# from jsonstat.version import __version__


# From cburgmer/pdfserver
# https://github.com/cburgmer/pdfserver/blob/master/setup.py
def parse_requirements(fname):
    requirements = []
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        for line in f:
            if re.match(r'\s*#', line):  # comment
                continue
            if re.match(r'\s*$', line):  # empty line
                continue
            elif re.match(r'\s*-f\s+', line):  # line starting with -f (find-links)
                continue
            elif re.match(r'\s*-r\s+', line):  # line starting with -r (include requirements)
                continue
            if re.match(r'\s*-e\s+', line):
                # TODO support version numbers
                requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
            else:
                requirements.append(line)
    return requirements


def parse_dependency_links(fname):
    dependency_links = []
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        for line in f:
            if re.match(r'\s*-[ef]\s+', line):
                dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links


# https://stackoverflow.com/questions/16367770/my-rst-readme-is-not-formatted-on-pypi-python-org
def yield_sphinx_only_markup(lines):
    """
    Cleans-up Sphinx-only constructs (ie from README.rst),
    so that *PyPi* can format it properly.

    To check for remaining errors, install ``sphinx`` and run::

            python setup.py --long-description | sed -file 'this_file.sed' | rst2html.py  --halt=warning

    :param file_inp:     a `filename` or ``sys.stdin``?
    :param file_out:     a `filename` or ``sys.stdout`?`

    """
    substs = [
        ## Selected Sphinx-only Roles.
        #
        (r':abbr:`([^`]+)`', r'\1'),
        (r':ref:`([^`]+)`', r'`\1`_'),
        (r':term:`([^`]+)`', r'**\1**'),
        (r':dfn:`([^`]+)`', r'**\1**'),
        (r':(samp|guilabel|menuselection):`([^`]+)`', r'``\2``'),

        ## Sphinx-only roles:
        #        :foo:`bar`   --> foo(``bar``)
        #        :a:foo:`bar` XXX afoo(``bar``)
        #
        # (r'(:(\w+))?:(\w+):`([^`]*)`', r'\2\3(``\4``)'),
        (r':(\w+):`([^`]*)`', r'\1(``\2``)'),

        ## Sphinx-only Directives.
        #
        (r'\.\. doctest', r'code-block'),
        (r'\.\. plot::', r'.. '),
        (r'\.\. seealso', r'info'),
        (r'\.\. glossary', r'rubric'),
        (r'\.\. figure::', r'.. '),

        ## Other
        #
        (r'\|version\|', r'x.x.x'),
    ]

    regex_subs = [(re.compile(regex, re.IGNORECASE), sub) for (regex, sub) in substs]

    def clean_line(line):
        regex, sub = (None, None)
        try:
            for (regex, sub) in regex_subs:
                line = regex.sub(sub, line)
        except Exception as ex:
            print("ERROR: %s, (line(%s)" % (regex, sub))
            raise ex

        return line

    for line in lines:
        yield clean_line(line)


def read_text_lines(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.readlines()


readme_lines = read_text_lines('README.rst')
long_desc = ''.join(yield_sphinx_only_markup(readme_lines))

# execfile is only python 2
# execfile('jsonstat/version.py')

# if sys.version_info >= (3,2):
#     install_requires = ["threadpool >= 1.2.7"]
# else:
#     install_requires = ["threadpool >= 1.2.3"]

setup(
    name="jsonstat.py",
    description='Library for reading JSON-stat format data.',
    long_description=long_desc,
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
        'Programming Language :: Python :: 3.6',
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

    include_package_data=True,
    package_data={
        'jsonstat': [
            'schemas/collection.json',
            'schemas/dataset.json',
            'schemas/dimension.json',
            'schemas/jsonstat.json',
        ],
    },

    data_files=[('', ['requirements.txt'])],

    install_requires=parse_requirements('requirements.txt'),
    # dependency_links=parse_dependency_links('requirements.txt'),
    tests_require=parse_requirements('requirements_for_test.txt'),

    entry_points={
        'console_scripts': [
            'jsonstat=jsonstat.cli.cli_jsonstat:cli',  # command=package.module:function
        ],
    },

)
