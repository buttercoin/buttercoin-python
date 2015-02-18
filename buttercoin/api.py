import json
import ssl
import time
import base64
import hashlib
import hmac
import urllib

import requests
from requests.adapters import HTTPAdapter

try:
    from requests.packages.urllib3.poolmanager import PoolManager
except ImportError:
    from urllib3.poolmanager import PoolManager

# buttercoin exceptions
from buttercoin import exceptions


class HTTPMethods(object):
    ''' HTTP methods that can be used with Buttercoin's API. '''

    GET = 'get'
    POST = 'post'
    DELETE = 'delete'


class ButtercoinAdapter(HTTPAdapter):
    ''' Adapt :py:mod:`requests` to Buttercoin. '''

    def init_poolmanager(self, connections, maxsize, block=False):
        ''' Initialize pool manager with forced TLSv1 support. '''

        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def fulfill(method, *args, **kwargs):
    ''' Fulfill an HTTP request to Buttercoin's API. '''

    s = requests.Session()
    s.mount('https://', ButtercoinAdapter())
    return getattr(s, method)(*args, **kwargs)


class ButtercoinApi(object):
    """
    Responsible for communicating with the Buttercoin API. Used also for async processing.
    """

    production_url = "https://api.buttercoin.com"
    sandbox_url = "https://sandbox.buttercoin.com"

    api_version = "v1"

    def __init__(self, api_key, api_secret, mode, api_version='v1'):
        self.api_key = api_key
        self.api_secret = api_secret

        if mode != 'production':
            self.base_url = self.sandbox_url
        else:
            self.base_url = self.production_url

        if api_version:
            self.api_version = api_version


    def _get_signature(self, verb, path, url, timestamp, body=None):
        """
        Performs the HMAC with SHA-256 signature of the timestamp, url, and params

        :param verb: string, the http request method to use 
        :param path: string, the api call path (e.g. orders)
        :param url: string, the url of the API call you're trying to make 
        :param timestamp: integer, UTC timestamp in ms, must be within 5 minutes of Buttercoin server time 
        :param body: JSON object, the request params
		"""

        if not body:
            body = {}

        if verb == HTTPMethods.POST and body:
            url += json.dumps(body)

        url = timestamp + url
        msg = base64.b64encode(url)
        msg = hmac.new(key=self.api_secret, msg=msg, digestmod=hashlib.sha256).digest()
        return base64.b64encode(msg)

    def _get_headers(self, signature, timestamp):
        """
        Builds the headers to use with each API call

        :param signature: string, the signed hash based on secret key, url and timestamp
		:param timestamp: integer, UTC timestamp in ms, must be within 5 minutes of Buttercoin server time 
        """
        headers = {
            "X-Buttercoin-Access-Key": self.api_key,
            "X-Buttercoin-Signature": signature,
            "X-Buttercoin-Date": int(timestamp),
            "Content-Type": 'application/json'
        }
        return headers

    def _perform_request(self, verb, path, timestamp=None, body=None, authenticate=True):
        if not body:
            body = {}

        # throw error if api key or api secret not included, but required
        if authenticate is True and (not self.api_key or not self.api_secret):
            raise exceptions.InvalidEnvironmentError(
                "API Key and API Secret are required for this operation."
            )

        url = self.base_url + "/" + self.api_version + "/" + path
        if verb == HTTPMethods.GET and body:
            url += "?" + '&'.join("%s=%s" % (key, urllib.quote(val).replace('%3A', ':')) for (key, val) in body.iteritems())

        if not timestamp:
            timestamp = unicode(int(round(time.time() * 1000)))

        headers = {}

        if authenticate:
            signature = self._get_signature(verb=verb, path=path, url=url, body=body, timestamp=timestamp)
            headers = self._get_headers(signature=signature, timestamp=timestamp)

        data = json.dumps(body) if verb == HTTPMethods.POST else None
        response = fulfill(verb, url, headers=headers, data=data)
        return self._process_response(response)

    def _process_response(self, response):
        val = None
        if response.status_code == 200:
            val = response.json()
        elif response.status_code == 201:
            val = {'status': response.status_code, 'message': 'This operation requires email confirmation'}
        elif response.status_code == 202:
            val = response.headers['location']
        elif response.status_code == 204:
            val = {'status': response.status_code, 'message': 'This operation has completed successfully'}
        elif response.status_code >= 400:
            error = response.json()
            raise exceptions.ButtercoinApiError(error)
        return val

    def get(self, path, timestamp=None, body=None, authenticate=True):
        if not body:
            body = {}

        return self._perform_request(HTTPMethods.GET, path=path, body=body, timestamp=timestamp,
                                     authenticate=authenticate)

    def post(self, path, timestamp=None, body=None):
        if not body:
            body = {}

        return self._perform_request(HTTPMethods.POST, path=path, body=body, timestamp=timestamp)

    def delete(self, path, timestamp=None):
        return self._perform_request(HTTPMethods.DELETE, path=path, timestamp=timestamp)
