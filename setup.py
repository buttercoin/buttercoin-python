#!/usr/bin/env python

from distutils.core import setup

setup(name="buttercoin",
      packages=["buttercoin"],
      version="1.0.0",
      description="Buttercoin API Python Client",
      author="Buttercoin",
      author_email="hello@buttercoin.com",
      url="https://github.com/buttercoin/buttercoin-python",
      keywords = ['bitcoin', 'buttercoin', 'trading platform', 'cryptocurrency', 'digital currency', 'btc'],
      install_requires=["requests", "jsonurl"],
      tests_require=["nose"]
)