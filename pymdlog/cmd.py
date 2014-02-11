"""
Command line module.
"""

from __future__ import absolute_import, print_function
from optparse import OptionParser
import sys

try:
    import matplotlib.pyplot as plt
except ImportError:
    HAS_PLOTLIB = False
else:
    HAS_PLOTLIB = True

    def save_plots(x, ys, xlb, ylbs, figname):
        """Plot multiple 2D line/point figures, which share a x-axis."""
        print('Generate figure %s' % figname)
        plt.close('all')
        n = len(ylbs)
        if n == 1:  # single plot
            _, ax = plt.subplots()
            ax.plot(x, ys[0], 'k-')
            ax.set_ylabel(ylbs[0])
        else:       # multiple plots
            _, axs = plt.subplots(n, sharex=True)
            for ax, y, ylb in zip(axs, ys, ylbs):
                ax.plot(x, y, 'k-')
                ax.set_ylabel(ylb)
        ax.set_xlabel(xlb)
        plt.savefig(figname, dpi=300)

from .gui import run_gui
from .analysis import LogAnalyzer
from .datfile import DatFile
from .csvfile import CsvFile


def main():
    """Parse the command line arguments."""
    # enter GUI mode if no arguments given
    if len(sys.argv) == 1:
        run_gui()
        return

    usage = 'Usage: pymdlog (GUI mode) or pymdlog [options] (Command-line mode)'
    parser = OptionParser(usage=usage, add_help_option=False)

    parser.add_option('-h', '--help',
                      action='help',
                      help='Show this help message and exit.')

    parser.add_option('-t', '--type',
                      type='choice',
                      dest='inptype',
                      choices=['amber', 'namd'],
                      default='amber',
                      help='Specify the input MD log file type: '
                           '"amber", "namd". [default: %default]')

    parser.add_option('-i', '--input',
                      dest='inploc',
                      help='Specify the input MD log file location(s). If more '
                           'than one file is specified, separate them with '
                           'comma.')

    parser.add_option('-o', '--output',
                      dest='outloc',
                      default='output.dat',
                      help='Specify the output result file location. The file '
                           'type is extension-detected. [default: %default]')

    parser.add_option('-f', '--figure',
                      dest='figloc',
                      help='Specify the output figure location. The file type '
                           'is extension-detected; ".png", ".eps", and ".pdf" '
                           'are supported. NOTE: Need matplotlib.')

    parser.add_option('-x', '--xaxis',
                      dest='x',
                      help='Specify the x-axis data set.')

    parser.add_option('-y', '--yaxis',
                      dest='y',
                      help='Specify the y-axis data set(s). If more than one '
                           'data set is specified, separate them with comma.')

    parser.disable_interspersed_args()
    opts, args = parser.parse_args()
    if args:
        raise ValueError("Unknown argument: " + args[0])

    # command-line mode
    run_cmd(opts)


def run_cmd(opts):
    """Command-line mode."""
    # sanity check
    # ------------
    if not opts.inploc:
        raise ValueError("Need input files.")
    else:
        inploc = opts.inploc.split(',')

    outloc = figloc = None
    if not opts.outloc and not opts.figloc:
        raise ValueError("Need output file or figure.")
    else:
        if opts.outloc:
            outloc = opts.outloc
        if opts.figloc:
            if not HAS_PLOTLIB:
                raise RuntimeError("Need matplotlib for plotting.")
            figloc = opts.figloc

    x = {'amber': 'TIME', 'namd': 'TS'}[opts.inptype] if not opts.x else opts.x
    y = opts.y.split(',') if opts.y else []

    # parse log file
    # ------------
    ana = LogAnalyzer(opts.inptype)
    data = ana.analyze(*inploc)
    for i in y:
        if i not in data:
            raise ValueError("Data set '%s' not found." % i)

    # generate output file and/or figure
    # ------------
    xdat = data[x]
    ydat = [data[i] for i in y] if y else [data[i] for i in data if i != x]

    if outloc:
        if outloc.lower().endswith('.csv'):
            CsvFile(outloc, 'w').write(xdat, *ydat)
        else:
            DatFile(outloc, 'w').write(xdat, *ydat)

    if HAS_PLOTLIB and figloc:
        save_plots(xdat, ydat, x, y, figloc)
