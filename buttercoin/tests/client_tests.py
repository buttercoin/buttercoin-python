import unittest
import base64
import json
import datetime
import requests
import os
import sys
from buttercoin import exceptions
import buttercoin
from buttercoin.client import ButtercoinClient

__author__ = 'kevin-buttercoin'

class ClientTests(unittest.TestCase):

    def setUp(self):
        super(ClientTests, self).setUp()
        buttercoin._client = None
        buttercoin.public_key = None
        buttercoin.secret_key = None

    def test_environment_setup(self):
        buttercoin._client = None
        buttercoin.public_key = None
        buttercoin.secret_key = None
        self.assert_raises(exceptions.InvalidEnvironmentError,
                            buttercoin.get_balances)
