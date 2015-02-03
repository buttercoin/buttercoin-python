#!/usr/bin/env python

from distutils.core import setup

setup(name="buttercoin",
      version="1.0.0",
      description="Buttercoin API Python Client",
      author="Buttercoin",
      author_email="hello@buttercoin.com",
      url="https://github.com/buttercoin/buttercoin-python",
      packages=["buttercoin"],
      install_requires=["requests", "jsonurl"],
      tests_require=["nose"]
)