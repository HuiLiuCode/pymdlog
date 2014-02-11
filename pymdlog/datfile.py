"""
Module to read and write simple text files.
"""

from __future__ import absolute_import, print_function
try:
    from future_builtins import zip
except ImportError:
    pass

from .basefile import TextFile

__all__ = ['DatFile']


class DatFile(TextFile):
    """Read and write dat files."""
    filetype = "simple text data"

    def write(self, xdat, *ydat, **fmt):
        """Write a single-x-multiple-y file for plotting.
        fmt: xfmt, yfmt, sep
        """
        super(DatFile, self).write()

        # sanity check
        xlen = len(xdat)
        for i, d in enumerate(ydat):
            ylen = len(d)
            if xlen != ylen:
                raise ValueError("$%d x=%d y=%d" % (i, xlen, ylen))

        xfmt = fmt.get('xfmt', 's')
        yfmt = fmt.get('yfmt', 's')
        sep = fmt.get('sep', ' ')
        fmt = '%' + xfmt + (sep + '%' + yfmt)*len(ydat) + '\n'

        for txt in zip(xdat, *ydat):
            self.fp.write(fmt % txt)

    def read(self):
        """Read a dat file."""
        super(DatFile, self).read()

        xdat, ydat = [], []

        for n, line in enumerate(self.fp):
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            xy = [float(i) for i in line.split()]
            if len(xy) < 2:
                raise RuntimeError('Found only one column in line ' + n)
            xdat.append(xy[0])
            ydat.append(xy[1:])
        return xdat, list(zip(*ydat))
