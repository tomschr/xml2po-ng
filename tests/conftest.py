#
#
#

from collections import defaultdict #, namedtuple
from itertools import groupby
# from pathlib import Path

import py
from py.path import local as Path

from lxml import etree
import pytest
import sys


DATADIR = Path(__file__).dirname


class GroupTransFiles(object):
    """A class which groups a set of translated files. This set contains:

    * .xml = the original, untranslated file as XML format
    * .pot = the PO template file which contains the strings to be translated
    * .po  = the translated PO file of a specific natural language
    * .xml.out = The translated result XML file
    """
    def __init__(self, path):
        self.grouped = defaultdict(list)
        self.path = Path(path)

    def _stem(self, fn):
        """Get the basename of the file (regardless if it is .xml or .xml.out

        :param fn: the filename with suffixes
        :return: the basename
        """
        if fn.strpath.endswith(".xml.out"):
            return fn.basename.replace('.xml.out', '')
        return fn.purbasename

    def _get_candidates(self):
        """Yields a file which contains one of the preferred file extensions
        """
        suffixes = ('.po', '.pot', '.xml', '.out')
        #for candidate in self.path.iterdir():
        #    if candidate.is_file() and (candidate.suffix in suffixes):
        #        yield candidate
        # -----
        yield from [candidate for candidate in self.path.iterdir()
                    if candidate.isfile() and (candidate.ext in suffixes)]

    def __iter__(self):
        """Iterator which yields grouped files

        A dictionary entry looks like this:

        'foo': [PosixPath('foo.pot'), PosixPath('foo.po'), PosixPath('foo.xml'), PosixPath('foo.xml.out')]

        :return: a tuple of key and value of the previous entry. The key is the basename
                 of the filename and the value the list of all filenames that belongs to
                 this basename
        """
        # Group the files related to the basename and store all related files to the
        # dictionary self.grouped:
        for key, group in groupby(self._get_candidates(), self._stem):
            for fn in group:
                self.grouped[key].append(fn)
        for key, value in self.grouped.items():
            yield key, value

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.path)

# DATA = GroupTransFiles(DATADIR)

def pytest_report_header(config):
    return "*** XML2PO Translation ***"


def pytest_collect_file(parent, path):
    config = parent.config
    base = path.purebasename
    if path.ext != ".xml":
        return
    suffixes = ('po', 'pot', 'xml.out')
    files = dict()
    # files['xml'] = path
    for ext in suffixes:
        p = path.new(ext=".%s" % ext)
        if p.exists():
            ext = 'out' if ext == 'xml.out' else ext
            files[ext] = p

    # print(">> %s" % base, file=sys.stderr)
    return XML2POFiles(base, parent, files)



class XMLPOException(ValueError):
    """ custom exception for error reporting. """


class XML2POFiles(pytest.Item, pytest.File):
    def __init__(self, path, parent=None, files=None):
        super().__init__(path, parent)
        self.add_marker("xml2po")
        self.files = files
        if files is None:
            files = {ext: None for ext in ('.po', '.pot', '.out')}

        for key, value in files.items():
            setattr(self, key.replace('.', ''), value)

    #def collect(self):
    #    parent = XMLPOItem('xml', self.fspath, self.parent)
    #    yield parent
    #    for fn in self.files.items():
    #        yield XMLPOItem(fn.ext.replace('.', ''), fn, parent)

    def runtest(self):
        call = py.io.StdCapture.call
        import random
        found_errors = random.choice([True, False])
        out="Huhu"
        err="Ach herrje!"
        found_errors, out, err = call(check_file, self.fspath, self.files)
        if found_errors:
            raise XMLPOException(out, err)

    def reportinfo(self):
        return (self.fspath, -1, "XML2PO-check" )

class XMLPOItem(pytest.Item):
    def __init__(self, suffix, name, parent):
        super().__init__(name, parent)
        self.suffix = suffix

def check_file(path, pep8ignore, max_line_length):
    checker = pep8.Checker(str(path), ignore=pep8ignore, show_source=1,
                           max_line_length=max_line_length)
    return checker.check_all()