"""
Statistical module.
"""

from __future__ import division, print_function
try:
    from future_builtins import zip
except ImportError:
    pass
from math import sqrt, fsum

__all__ = ['ITEMS', 'calc_stats', 'save_stats']

ITEMS = ('Title', 'Population', 'Mean', 'SD', 'SEM', 'Max', 'Min', 'CI95%')


def mean(data):
    """Calculate the mean value."""
    return fsum(data) / len(data)


def sd(data):
    """Calculate the standard deviation (SD)."""
    avg = mean(data)
    sum_sq_diff = fsum((i-avg)**2 for i in data)
    return sqrt(sum_sq_diff / len(data))


def sem(data):
    """Calculate the standard error of the mean (SEM)."""
    return sd(data) / sqrt(len(data))


def ci95(data):
    """Calculate the 95% confidence interval."""
    m = mean(data)
    d = 1.96*sem(data)
    return m-d, m+d


def calc_stats(titles, data):
    """Calculate statistical results."""
    return [(t, len(d), mean(d), sd(d), sem(d), max(d), min(d),
            '(%s, %s)'%ci95(d))
            for t, d in zip(titles, data)]


def save_stats(data, fname='stats.log'):
    """Save statistical results in a file."""
    print('Write statistical data file %s' % fname)
    fmt = '"%s"' + ' %s'*(len(ITEMS)-1) + '\n'
    with open(fname, 'w') as f:
        f.write(' '.join(ITEMS)+'\n')
        for d in data:
            f.write(fmt % tuple(d))
