"""
Module to read and write MS Excel compatible CSV files.
"""

from __future__ import absolute_import
try:
    from future_builtins import zip
except ImportError:
    pass
import csv
import sys
IS_PY3 = sys.version_info.major >= 3

from .basefile import TextFile

__all__ = ['CsvFile']


class CsvFile(TextFile):
    """MS Excel compatible CSV file."""
    filetype = "MS Excel compatible CSV"
    modes = {'r': 'r', 'w': 'w'} if IS_PY3 else {'r': 'r', 'w': 'wb'}

    def open(self, *args, **kwargs):
        # py3 has a newline argument for open, however, in py2, the text
        # file has to be opened with 'wb' to prevent the translation of
        # end-of-line character.
        if IS_PY3:
            return open(newline='\n', *args, **kwargs)
        return super(CsvFile, self).open(*args, **kwargs)

    def write(self, xdat, *ydat):
        super(CsvFile, self).write()
        writer = csv.writer(self.fp, dialect='excel')
        for d in zip(xdat, *ydat):
            writer.writerow(d)

    def read(self):
        super(CsvFile, self).read()
        reader = csv.reader(self.fp)
        return [d for d in reader]
