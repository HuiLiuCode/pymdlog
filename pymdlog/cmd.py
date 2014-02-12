"""
Command line module.
"""

from __future__ import absolute_import, print_function
from argparse import ArgumentParser
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

from . import __program__ as NAME, __version__ as VER
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

    parser = ArgumentParser(prog=NAME.lower(), add_help=False,
                            description='These arguments are used in the '
                                        'command-line mode. If nothing is '
                                        'given, the GUI mode will be used.')

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-h', '--help', action='help',
                       help='Show this help message and exit.')

    group.add_argument('-v', '--version', action='version',
                       help="Show program's version and exit.",
                       version='%s, Version %s'%(NAME, VER))

    group.add_argument('-i', '--input', dest='inploc', nargs='+',
                       help='Specify the input MD log file location(s). '
                            '[required]')

    parser.add_argument('-t', '--type', dest='inptype',
                        choices=['amber', 'namd'], default='amber',
                        help='Specify the input MD log file type. '
                             '[default: %(default)s]')

    parser.add_argument('-x', '--xaxis', dest='x',
                        help='Specify the x-axis data set. '
                             '[default: TIME for Amber, TS for NAMD]')

    parser.add_argument('-y', '--yaxis', dest='y', nargs='+',
                        help='Specify the y-axis data set(s). '
                             '[default: all data sets found except X]')

    parser.add_argument('-o', '--output', dest='outloc', default='output.dat',
                        help='Specify the output result file location. The '
                             'file type is extension-detected. '
                             '[default: %(default)s]')

    parser.add_argument('-f', '--figure', dest='figloc',
                        help='Specify the output figure location. The file '
                             'type is extension-detected. png, eps and pdf '
                             'are supported. [NOTE: need matplotlib]')

    # command-line mode
    run_cmd(parser.parse_args())


def run_cmd(args):
    """Command-line mode."""
    if args.figloc and not HAS_PLOTLIB:
        raise RuntimeError("Need matplotlib for plotting.")

    x = {'amber': 'TIME', 'namd': 'TS'}[args.inptype] if not args.x else args.x
    y = args.y if args.y else []

    # parse log file
    # ------------
    ana = LogAnalyzer(args.inptype)
    data = ana.analyze(*args.inploc)
    for i in y:
        if i not in data:
            raise ValueError("Data set '%s' not found." % i)

    # generate output file and/or figure
    # ------------
    xdat = data[x]
    ydat = [data[i] for i in y] if y else [data[i] for i in data if i != x]

    if args.outloc.lower().endswith('.csv'):
        CsvFile(args.outloc, 'w').write(xdat, *ydat)
    else:
        DatFile(args.outloc, 'w').write(xdat, *ydat)

    if args.figloc:
        save_plots(xdat, ydat, x, y, args.figloc)
