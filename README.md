## PyMDLog

PyMDLog is a Python-powered tool for analyzing log files generated by molecular
dynamics (MD) simulation packages.

### Introduction

I use MD packages, such as [Amber][] and [NAMD][], in my research work. Each of
them generates log files (mdout in Amber's terminology) while computing.
Properties of the simulation system are recorded in the files. There are
existing scripts for parsing them, like process_mdout.perl for Amber and
namdplot for NAMD. However, I'm not satisfied with them. So I wrote this tool
and made it publicly available. I found it useful and hope it is also helpful
to you.

[Amber]: http://ambermd.org/
[NAMD]: http://www.ks.uiuc.edu/Research/namd/

### Prerequisites

* [Python](http://www.python.org/) 2.7, 3.2-3.3

* [matplotlib](http://matplotlib.org/) (optional, for plotting)

### Installation

Once you have satisfied the requirements, run this command from the command
prompt:

    $ python setup.py install

### Usage

Make sure `PYTHONHOME/Scripts` is in the `PATH` environment variable. Then
run this command:

    $ pymdlog

You will see a GUI which is fairly self-explanatory.

Or if you want to use the command-line mode, do things like this:

    $ pymdlog -i 1.out 2.out -t amber -x TIME -y Etot "1-4 NB" -o result.dat

    $ pymdlog -i 1.log 2.log -t namd -x TS -y BOND ANGLE -f result.png

For more information about the arguments, run

    $ pymdlog -h

If you haven't installed matplotlib or don't like the generated figure, you
can use the output file with your favorite plotting software:

* `Simple` for Gnuplot, xmgrace, R (`read.table` with `header=FALSE`), Origin

* `CSV` for Excel

The above-mentioned have been tested, however, other programs should be
compatible too.

### Bug Report

If you have any questions about using this program or find a bug, please feel
free to contact me via email:
teffliu@hotmail.com
