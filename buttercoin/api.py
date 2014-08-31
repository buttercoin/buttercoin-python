# stdlib
import json
import jsonurl
import ssl
import time
import base64
import hashlib
import hmac

# requests
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

# buttercoin exceptions
from buttercoin import exceptions


__author__ = 'kevin-buttercoin'


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

    # the default base URL of the Buttercoin API
    production_url = "https://api.buttercoin.com"
    sandbox_url = "https://sandbox.buttercoin.com"
    # the default version of the Buttercoin API
    api_version = "v1"

    # self says it belongs to ButtercoinApi/andOr is the object passed into ButtercoinApi
    # __init__ create buttercoinapi object whenever ButtercoinApi class is invoked
    def __init__(self, public_key=None, secret_key=None, mode='production', api_version='v1'):
        """
        Initializes a ButtercoinApi object

        :param public_key: API Public Key
        :param secret_key: API Secret Key
        :param base_url: optional, set this to override where API requests are sent
        :param api_version: string, optional, set this to override what API version is used
        """
        # super? recreates the object with values passed into ButtercoinApi
        super(ButtercoinApi, self).__init__()
        self.public_key = public_key
        self.secret_key = secret_key

        if mode != 'production':
            self.base_url = self.sandbox_url
        else:
            self.base_url = self.production_url
        if api_version:
            self.api_version = api_version

    def _build_url(self, verb, path, body={}):
        """
        Builds the API url from the baseUrl and the endpoint

        :param verb: string, the http request method to use 
        :param path: string, the api call path (e.g. orders)
        :param body: JSON object, the request params
        """
        url = self.base_url + "/" + self.api_version + "/" + path
        if verb == HTTPMethods.GET and body:
            url += "?" + jsonurl.query_string(body)
        return url
  
    def _get_signature(self, verb, path, url, timestamp, body={}):
        """
        Performs the HMAC with SHA-256 signature of the timestamp, url, and params

        :param verb: string, the http request method to use 
        :param path: string, the api call path (e.g. orders)
        :param url: string, the url of the API call you're trying to make 
        :param timestamp: integer, UTC timestamp in ms, must be within 5 minutes of Buttercoin server time 
        :param body: JSON object, the request params
		"""
        if verb == HTTPMethods.POST and body:
            url += json.dumps(body)
        url = timestamp + url
        msg = base64.b64encode(url)
        msg = hmac.new(key=self.secret_key, msg=msg, digestmod=hashlib.sha256).digest()
        return base64.b64encode(msg)

    def _get_headers(self, signature, timestamp):
        """
        Builds the headers to use with each API call

        :param signature: string, the signed hash based on secret key, url and timestamp
		:param timestamp: integer, UTC timestamp in ms, must be within 5 minutes of Buttercoin server time 
        """
        headers = {
            "X-Buttercoin-Access-Key": self.public_key,
            "X-Buttercoin-Signature": signature,
            "X-Buttercoin-Date": int(timestamp),
            "Content-Type": 'application/json'
        }
        return headers

    def _perform_request(self, verb, path, timestamp=None, body={}, authenticate=True):
        # throw error if public or secret key not included, but required
        if authenticate is True and (not self.public_key or not self.secret_key):
            raise exceptions.InvalidEnvironmentError(
                "Public Key and Secret Key are required for this operation."
            )

        url = self._build_url(verb=verb, path=path, body=body)
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
            val = { 'status': response.status_code, 'message': 'This operation requires email confirmation'}
        elif response.status_code == 202:
            val = response.headers['location']
        elif response.status_code == 204:
            val = { 'status': response.status_code, 'message': 'This operation has completed successfully'}
        elif response.status_code >= 400:
            error = response.json()
            raise exceptions.ButtercoinApiError(error)
        return val

    def get(self, path, timestamp=None, body={}, authenticate=True):
        return self._perform_request(HTTPMethods.GET, path=path, body=body, timestamp=timestamp, authenticate=authenticate)

    def post(self, path, timestamp=None, body={}):
        return self._perform_request(HTTPMethods.POST, path=path, body=body, timestamp=timestamp)

    def delete(self, path, timestamp=None):
        return self._perform_request(HTTPMethods.DELETE, path=path, timestamp=timestamp)
