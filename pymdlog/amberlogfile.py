"""
Module to parse AMBER output files.
"""

from __future__ import absolute_import
import collections
import re
import warnings

from .basefile import ReadOnlyTextFile

__all__ = ['AmberLogFile']

# "   4.  RESULTS"
PAT_BEGIN = re.compile(r'\s+\d\.\s+RESULTS\b')

# "TITLE = NUMBER"
# something like "NSTEP", "1-4 NB", "TIME(PS)", ignore the units
TITLE = r'\s+(?P<title>(\d-\d )?[a-zA-Z]+)(\([a-zA-Z]+\))?'
EQ = r'='
NUMBER = r'(?P<value>[+-]?([1-9]\d*\.\d*|0?\.\d*|[1-9]\d*|0))'
PAT_ITEM = re.compile(TITLE + r'\s*' + EQ + r'\s*' + NUMBER)

# "      A V E R A G E S   O V E R"
PAT_END = re.compile(r'\s+A V E R A G E S   O V E R')


class AmberLogFile(ReadOnlyTextFile):
    """Parse an AMBER (including CHAMBER) mdout file."""
    filetype = "AMBER mdout"

    def __init__(self, *args, **kwargs):
        super(AmberLogFile, self).__init__(*args, **kwargs)
        self.pat_begin = PAT_BEGIN
        self.pat_item = PAT_ITEM
        self.pat_end = PAT_END

    def read(self):
        super(AmberLogFile, self).read()
        data = collections.defaultdict(list)

        # forward the generator to the "RESULTS" section
        for line in self.fp:
            if self.pat_begin.match(line) is not None:
                break
        else:
            # can't find the beginning tag, which means a invalid file
            raise RuntimeError("Invalid %s file: '%s'" % (
                               self.filetype, self.filename))

        # parse data
        for line in self.fp:
            if not line.startswith(' '):
                continue
            items = self.pat_item.finditer(line)
            for i in items:
                k, v = i.group('title'), i.group('value')
                try:
                    n = int(v)
                except ValueError:
                    n = float(v)
                data[k].append(n)
            if self.pat_end.match(line) is not None:
                break
        else:
            # can't find the ending tag, which means a broken file
            warnings.warn("Broken %s file: '%s'" % (
                          self.filetype, self.filename))

        self.data = data
        return self.data
