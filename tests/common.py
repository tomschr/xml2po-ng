#
#
#
from collections import defaultdict
from itertools import groupby
# import shlex
import subprocess
from pathlib import Path


def cmpnodes(node1, node2):
    """Compare two nodes

    Two nodes (node1 and node2) are considered the same when the
    following rules apply:
    1. All attribute names from node1 are the same as in node2.
    2. All attribute values from node1 are the same as in node2.
    3. The tag name from node1 is the same as in node2.
    4. The namespace of the tag name from node1 is the same as in node2.

    Any child elements are not considered also additional namespace declarations.

    Examples:
    >>> n1 = etree.XML("<foo b='2' a='1'/>")
    >>> n2 = etree.XML("<foo a='1' b='2'/>")
    >>> compare_nodes(n1, n2)
    True
    >>> n1 = etree.XML("<foo a='10' xmlns='urn:x-foo'/>")
    >>> n2 = etree.XML("<d:foo xmlns:d='urn:x-foo' a='1O'/>")
    >>> compare_nodes(n1, n2)
    True
    >>> n1 = etree.XML("<foo a='10' xmlns:x="x" xmlns='urn:x-foo'/>")
    >>> n2 = etree.XML("<d:foo xmlns:d='urn:x-foo' a='1O'/>")
    >>> compare_nodes(n1, n2)
    True

    :param node1: first node
    :param node2: second node
    :return: True if two nodes are the same, otherwise not
    :rtype: bool
    """
    cmpns = node1.nsmap.get(node1.prefix) == node2.nsmap.get(node2.prefix)
    cmpattrs = node1.attrib == node2.attrib
    cmptags = node1.tag == node2.tag

    return cmpns and cmpattrs and cmptags


class XML2POTError(subprocess.SubprocessError):
    pass


def create_pot_from_xml(xmlfile, potfile=None):
    """Convert a XML file into a POT file

    $ xml2po -o chapter1.pot chapter1.xml

    :param xmlfile: the XML file
    :param potfile: If None, the POT file is created by removing the ".xml"
                    extension and adding ".pot"
    :raises: XML2POTError, if the xml2po command created an error
    """
    potarg = ''
    if potfile is None:
        potfile = xmlfile.rsplit(".xml", 1)[0] + ".pot"
        potarg = "-o %s " % potfile
    cmd = "xml2po %s%s" % (potarg, xmlfile)
    # cmd = shlex.split(cmd)
    proc = subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode:
        raise XML2POTError(err.decode('utf-8'))
    return out.decode('utf-8')


def create_translation(pofile, xmlfile, outxmlfile=None):
    """Create the translated XML from PO file and original XML file

    :param pofile: the translated PO file
    :param xmlfile: the original XML file (untranslated)
    :param outxmlfile: the translated, generated XML file or None (=stdout)
    :raises: XML2POTError, if the xml2po command created an error
    """
    outarg = ''
    if outxmlfile is None:
        outxmlfile = xmlfile.rsplit(".xml", 1)[0] + "-trans.xml"
        outarg = " > %s" % outxmlfile
    cmd = "xml2po -p %s %s %s" % (pofile, xmlfile, outarg)
    # cmd = shlex.split(cmd)
    proc = subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode:
        raise XML2POTError(err.decode('utf-8'))
    return out.decode('utf-8')


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
        s = fn.suffixes
        stem = fn.stem if len(s) == 1 else Path(fn.stem).stem
        return stem

    def _get_candidates(self):
        """Yields a file which contains one of the preferred file extensions
        """
        suffixes = ('.po', '.pot', '.xml', '.out')
        #for candidate in self.path.iterdir():
        #    if candidate.is_file() and (candidate.suffix in suffixes):
        #        yield candidate
        # -----
        yield from [candidate for candidate in self.path.iterdir()
                    if candidate.is_file() and (candidate.suffix in suffixes)]

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


if __name__ == "__main__":
    for app in GroupTransFiles("."):
        print(app)