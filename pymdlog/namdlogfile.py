"""
Module to parse NAMD log files.
"""

from __future__ import absolute_import
try:
    from future_builtins import zip
except ImportError:
    pass

from .basefile import ReadOnlyTextFile

__all__ = ['NamdLogFile']


class NamdLogFile(ReadOnlyTextFile):
    """Parse a NAMD log file."""
    filetype = "NAMD log"

    def read(self):
        super(NamdLogFile, self).read()
        self.titles = self.read_etitle()
        #self.fp.seek(0)
        self.values = self.read_energy()
        self.data = dict(zip(self.titles, zip(*self.values)))
        return self.data

    def read_etitle(self):
        for line in self.fp:
            if line.startswith('ETITLE:'):
                titles = line.split()[1:]
                break
        else:
            raise RuntimeError('No energy items found.')
        return titles

    def read_energy(self):

        def to_number(x):
            try:
                n = int(x)
            except ValueError:
                n = float(x)
            return n

        n = len(self.titles)
        data = []
        for i, line in enumerate(self.fp):
            if line.startswith('ENERGY:'):
                val = [to_number(x) for x in line.split()[1:]]
                if len(val) != n:
                    raise RuntimeError('File broken at line %d' % (i+1))
                data.append(val)
        return data
