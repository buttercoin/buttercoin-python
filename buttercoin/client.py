import base64
import json
from buttercoin import exceptions
from buttercoin.api import ButtercoinApi

__author__ = 'kadams'

class ButtercoinClient(object):
    """ The Buttercoin Client is the main object to use to interface with the Buttercoin API. It
    requires a public_key and private_key.

    POST requests will timeout after 305 seconds by default.
    """

    def __init__(self, public_key=None, secret_key=None, mode="production", api_class=ButtercoinApi):
        """ Initializes a ButtercoinClient object.

        :param public_key: API Public Key
        :param secret_key: API Secret Key
        :param mode: sandbox or production
        """
        super(ButtercoinClient, self).__init__()

        # Set up an api client to be used for querying 
        self.api = api_class(public_key=public_key, secret_key=secret_key, mode=mode)

        self.public_key = public_key
        self.secret_key = secret_key
        self.mode = mode

    def get_ticker(self):
        """
		Gets the ticker info, include last price, current bid and current ask
		"""
        return self.api.get('ticker', None, {}, False)

    def get_order_book(self):
        """
		Gets the order book with all current bids and asks
		"""
        return self.api.get('orderbook', None, {}, False)

    def get_key(self, timestamp=None):
        """
		Gets the permissions associated with the given public key
		"""
        return self.api.get('key', timestamp)["permissions"]
  
    def get_balances(self, timestamp=None):
        """
        Gets the balances associated with the account
        """
        return self.api.get('account/balances', timestamp)

    def get_deposit_address(self, timestamp=None):
        """
        Gets the balances associated with the account
        """
        return self.api.get('account/depositAddress', timestamp)["address"]

    def get_orders(self, body={}, timestamp=None):
        """
        Performs an order query returning a list of orders

           Returns the orders that meet the given criteria.

           :param body: json, JSON object containing the query parameters
        """
        return self.api.get('orders', timestamp, body)["results"]

    def get_order_by_id(self, order_id, timestamp=None):
        """
        Performs an order query

        Returns a single order with the given id.

        :param order_id: string, the id of the single order
        """
        path = "orders/{0}".format(order_id)
        return self.api.get(path, timestamp)

    def get_order_by_url(self, url, timestamp=None):
        """
        Performs an order query

        Returns a single transaction with the given id.

        :param url: string, the url for the order query
        """
        pos = url.rfind("orders/")
        path = url[pos:]
        return self.api.get(path, timestamp)

    def get_transactions(self, body={}, timestamp=None):
        """
        Performs an transaction query returning a list of transactions

        Returns the transactions that meet the given criteria.

        :param body: json, JSON object containing the query parameters
        """
        return self.api.get('transactions', timestamp, body)["results"]

    def get_transaction_by_id(self, transaction_id, timestamp=None):
        """
        Performs an transaction query

        Returns a single transaction with the given id.

        :param order_id: string, the id of the single transaction
        """
        path = "transactions/{0}".format(transaction_id)
        return self.api.get(path, timestamp)
    
    def get_transaction_by_url(self, url, timestamp=None):
        """
        Performs an transaction query

        Returns a single transaction with the given id.

        :param url: string, the url for the transaction query
        """
        pos = url.rfind("transactions/")
        path = url[pos:]
        return self.api.get(path, timestamp)

    def create_order(self, body={}, timestamp=None):
        """
        Create a new order

        Returns a string of the response location header url

        :param body: json, JSON object containing the order parameters
        """
        return self.api.post('orders', timestamp, body)

    def create_deposit(self, body={}, timestamp=None):
        """
        Create a new deposit of a fiat currency
        
        Returns a string of the response location header url

        :param body: json, JSON object containing the transaction parameters
        """
        return self.api.post('transactions/deposit', timestamp, body)

    def create_withdrawal(self, body={}, timestamp=None):
        """
        Create a new withdrawal of a fiat currency
        
        Returns a string of the response location header url or message that op requires confirmation

        :param body: json, JSON object containing the transaction parameters
        """
        return self.api.post('transactions/withdraw', timestamp, body)

    def send_bitcoin(self, body={}, timestamp=None):
        """
        Create a new transaction to send bitcoin to an address
        
        Returns a string of the response location header url or message that op requires confirmation

        :param body: json, JSON object containing the transaction parameters
        """
        return self.api.post('transactions/send', timestamp, body)

    def cancel_order(self, order_id, timestamp=None):
        """
        Cancel an order with the given id

        Returns json object containing status 204 with success message

        :param order_id: string, the id of the order to delete
        """
        path = "orders/{0}".format(order_id)
        return self.api.delete(path, timestamp)

    def cancel_transaction(self, transaction_id, timestamp=None):
        """
        Cancel an transaction with the given id

        Returns json object containing status 204 with success message

        :param order_id: string, the id of the transaction to delete
        """
        path = "transactions/{0}".format(transaction_id)
        return self.api.delete(path, timestamp)
