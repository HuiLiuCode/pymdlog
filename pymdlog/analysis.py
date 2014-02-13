"""
Analysis of log files.
"""

from __future__ import absolute_import
import collections
import warnings

from .amberlogfile import AmberLogFile
from .namdlogfile import NamdLogFile

__all__ = ['LogAnalyzer']


class LogAnalyzer(object):
    """Analyzing AMBER (including CHAMBER) mdout and NAMD log files."""

    def __init__(self, type):
        # currently support 'amber' and 'namd'.
        self.data = None
        self.type = type.lower()
        try:
            self.func = {
                    'amber': analyze_amber_log,
                    'namd': analyze_namd_log
                    }[self.type]
        except KeyError:
            raise ValueError("Unsupported file type %s" % type)

    def analyze(self, *filename):
        self.data = self.func(*filename)
        return self.data


def analyze_amber_log(*filename):
    """Analyzing Amber mdout file."""
    data = collections.defaultdict(list)
    for f in filename:
        newdata = AmberLogFile(f).read()
        for k, v in newdata.items():
            data[k].extend(v)

    nframe = len(data['TIME'])
    if nframe == 0:
        raise RuntimeError("No data found.")

    to_del = []
    for k, v in data.items():
        if len(v) != nframe:
            warnings.warn(
                    "Number of '%s' data frames is not equal to 'NSTEP'. "
                    "This item is meaningless and will be removed." % k)
            to_del.append(k)
    for k in to_del:
        del data[k]

    if len(data) <= 1:
        raise RuntimeError("No data left.")
    return data


def analyze_namd_log(*filename):
    """Analyzing NAMD log file."""
    data = collections.defaultdict(list)
    for f in filename:
        newdata = NamdLogFile(f).read()
        for k, v in newdata.items():
            data[k].extend(v)

    nframe = len(data['TS'])
    if nframe == 0:
        raise RuntimeError("No data found.")

    to_del = []
    for k, v in data.items():
        if len(v) != nframe:
            warnings.warn(
                    "Number of '%s' data frames is not equal to 'TS'. "
                    "This item is meaningless and will be removed." % k)
            to_del.append(k)
    for k in to_del:
        del data[k]

    if len(data) <= 1:
        raise RuntimeError("No data left.")
    return data
