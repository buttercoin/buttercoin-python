#!/usr/bin/env python

from distutils.core import setup

setup(name="buttercoin",
      version="0.0.1",
      description="Python Client for Buttercoin API",
      author="Buttercoin",
      author_email="kevin@buttercoin.com",
      url="https://github.com/buttercoin/buttercoinsdk-python",
      packages=["buttercoin"],
      install_requires=["requests", "pycrypto", "jsonurl"],
      tests_require=["nose"]
)
