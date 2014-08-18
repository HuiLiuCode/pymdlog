#!/usr/bin/env python

from distutils.core import setup
import sys
import os

package = "pymdlog"
name = __import__(package).__program__.lower()
version = __import__(package).__version__
description = __import__(package).__desc__
author = __import__(package).__author__
author_email = __import__(package).__email__
url = __import__(package).__url__
license = __import__(package).__license__

if sys.argv[1] == "sdist":
    scripts = ["scripts/pymdlog", "scripts/pymdlogwin.bat", "scripts/pymdlog.bat"]
else:
    if os.name == "nt":
        scripts = ["scripts/pymdlogwin.bat", "scripts/pymdlog.bat"]
    else:
        scripts = ["scripts/pymdlog"]

setup(
    name=name,
    version=version,
    description=description,
    long_description=open("README.md").read(),
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    packages=[package],
    scripts=scripts,
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Scientific/Engineering :: Chemistry"
        ]
    )
