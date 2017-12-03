#!/usr/bin/env python
#
# Copyright (c) 2017 SUSE Linux GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact SUSE LLC.
#
# To contact SUSE about this file by physical or electronic mail,
# you may find current contact information at www.suse.com


import io
import os
import os.path
import re

from setuptools import setup, find_packages

__projectname__ = "xml2po-ng"
__programname__ = ""
# __version__ will be read from sdsc/__init__.py
__authors__ = "Thomas Schraitle"
__license__ = "LGPL-2.1+"
__description__ = "Create a PO template from a DocBook XML file and merge it back into a translated XML file"

HERE = os.path.abspath(os.path.dirname(__file__))


def requires(filename):
    """Returns a list of all pip requirements

    :param filename: the Pip requirement file (usually 'requirements.txt')
    :return: list of modules
    :rtype: list
    """
    modules = []
    with open(filename, 'r') as pipreq:
        for line in pipreq:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            # if line.startswith('-r'):
            # TODO: what to do here?
            modules.append(line)
    return modules


def read(*names, **kwargs):
    """Read in file
    """
    with io.open(os.path.join(HERE, *names),
                 encoding=kwargs.get("encoding", "utf8")) as fp:
        return fp.read()


def find_version(*file_paths):
    """Read __version__ string from file paths

    :return: version string
    :rtype: str
    """
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setupdict = dict(
    name=__projectname__,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://python-packaging-user-guide.readthedocs.org/en/latest/single_source_version/
    version=find_version("src", "xml2pong", "__init__.py"),  # __version__,

    description=__description__,
    # long_description="",

    # The project's main homepage.
    url='https://www.github.org/tomschr/xml2po-ng',
    download_url='https://github.org/tomschr/xml2po-ng/releases',

    # Author details
    author=__authors__,
    author_email='toms@suse.de',

    license=__license__,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   1 - Planning
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 1 - Planning',

        # Indicate who your project is intended for
        'Topic :: Documentation',
        'Topic :: Text Processing',
        'Topic :: Utilities',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development :: Documentation',
        'Intended Audience :: Developers',
        'Intended Audience :: Translators',
        'Natural Language :: English',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',

        # Supported Python versions
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',        
    ],

    keywords=["docbook", "translation", "xml2po", "xml", "gettext"],

    # ----
    # Includes data files from MANIFEST.in
    #
    # See also:
    # http://stackoverflow.com/a/16576850
    # https://pythonhosted.org/setuptools/setuptools.html#including-data-files
    include_package_data=True,

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # toms: Check this
    packages=find_packages('src'),
    package_dir={'': 'src'},

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=requires('requirements.pip'),


    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': ['xml2pong=xml2pong.cli:main'],
    },

    # Required packages for using "setup.py test"
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'pytest-catchlog'],
)


# Call it:
setup(**setupdict)

# EOF
