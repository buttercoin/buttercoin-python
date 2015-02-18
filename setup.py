#!/usr/bin/env python

from __future__ import print_function

try:
    from setuptools import setup

    extra = dict(test_suite="tests.test.suite", include_package_data=True)
except ImportError:
    from distutils.core import setup

    extra = {}

import sys

from buttercoin import __version__

if sys.version_info <= (2, 5):
    error = "ERROR: buttercoin requires Python Version 2.6 or above...exiting."
    print(error, file=sys.stderr)
    sys.exit(1)


def readme():
    with open("README.rst") as f:
        return f.read()


setup(name="buttercoin",
      version=__version__,
      description="Buttercoin API Python Client",
      long_description=readme(),
      author="Buttercoin",
      author_email="hello@buttercoin.com",
      maintainer="Buttercoin",
      maintainer_email="api@buttercoin.com",
      url="https://github.com/buttercoin/buttercoin-python",
      bugtrack_url="https://github.com/buttercoin/buttercoin-python/issues",
      packages=["buttercoin"],
      license="MIT",
      platforms="Posix; MacOS X; Windows",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Internet",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 2.6",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4"],
      keywords=['bitcoin', 'buttercoin', 'trading platform', 'cryptocurrency', 'digital currency', 'btc'],
      install_requires=["requests"],
      tests_require=["nose"]
)
