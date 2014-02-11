"""
Base file objects.
"""

from __future__ import absolute_import, print_function
import os

__all__ = ['ReadOnlyTextFile', 'TextFile']


class BaseFile(object):
    """Base class."""

    def __init__(self, filename, mode='r'):
        self.mode = mode
        try:
            mode = self.modes[mode]
        except KeyError:
            raise ValueError("Require mode %s" % ", ".join(self.modes))

        self.fp = self.open(filename, mode)
        self.filename = os.path.basename(filename)

    def __del__(self):
        self.close()

    def open(self, *args, **kwargs):
        """Open the file."""
        return open(*args, **kwargs)

    def close(self):
        """Close the file."""
        self.fp.close()

    def __enter__(self):
        """For context manager
        with XxxFile(filename) as f:
            BLOCK
        """
        return self

    def __exit__(self, type, value, traceback):
        """For context manager"""
        self.close()


def iread(self):
    """Readable interface."""
    if self.mode != "r":
        raise RuntimeError("File can only be read with mode 'r'.")
    print("Read %s file %s" % (self.filetype, self.filename))


def iwrite(self):
    """Writable interface."""
    if self.mode != "w":
        raise RuntimeError("File can only be written with mode 'w'.")
    print("Write %s file %s" % (self.filetype, self.filename))


class TextFile(BaseFile):
    """Class with methods to read and write text files."""
    modes = {'r': 'r', 'w': 'w'}
    read = iread
    write = iwrite


class ReadOnlyTextFile(BaseFile):
    """Class with method to read text files."""
    modes = {'r': 'r'}
    read = iread
