import os
from buttercoin.client import ButtercoinClient

__version__ = '1.0.2'

_client = None
api_key = None
api_secret = None
mode = None


def _initialize_client_from_environment():
    global _client, api_key, api_secret, mode

    if _client is None:
        api_key = api_key or os.environ.get("BUTTERCOIN_API_KEY")
        api_secret = api_secret or os.environ.get("BUTTERCOIN_API_SECRET")
        mode = mode or os.getenv("BUTTERCOIN_MODE", "production")

        _client = ButtercoinClient(api_key=api_key,
                                   api_secret=api_secret,
                                   mode=mode)


def get_ticker(timestamp=None):
    _initialize_client_from_environment()
    return _client.get_ticker(timestamp=timestamp)


def get_orderbook(timestamp=None):
    _initialize_client_from_environment()
    return _client.get_orderbook(timestamp=timestamp)


def get_trade_history(timestamp=None):
    _initialize_client_from_environment()
    return _client.get_trade_history(timestamp=timestamp)


def get_key(timestamp=None):
    _initialize_client_from_environment()
    return _client.get_key(timestamp=timestamp)


def get_balances(timestamp=None):
    _initialize_client_from_environment()
    return _client.get_balances(timestamp=timestamp)


def get_deposit_address(timestamp=None):
    _initialize_client_from_environment()
    return _client.get_deposit_address(timestamp=timestamp)


def get_orders(body=None, timestamp=None):
    if not body:
        body = {}

    _initialize_client_from_environment()
    return _client.get_orders(body=body, timestamp=timestamp)


def get_order_by_id(order_id, timestamp=None):
    _initialize_client_from_environment()
    return _client.get_order(order_id, timestamp=timestamp)


def get_order_by_url(url, timestamp=None):
    _initialize_client_from_environment()
    return _client.get_order_by_url(url, timestamp=timestamp)


def get_transactions(body=None, timestamp=None):
    if not body:
        body = {}

    _initialize_client_from_environment()
    return _client.get_transactions(body=body, timestamp=timestamp)


def get_transaction_by_id(transaction_id, timestamp=None):
    _initialize_client_from_environment()
    return _client.get_transaction_by_id(transaction_id, timestamp=timestamp)


def get_transaction_by_url(url, timestamp=None):
    _initialize_client_from_environment()
    return _client.get_transaction_by_url(url, timestamp=timestamp)


def create_order(data=None, timestamp=None):
    if not data:
        data = {}

    _initialize_client_from_environment()
    return _client.create_order(data=data, timestamp=timestamp)


def create_deposit(data=None, timestamp=None):
    if not data:
        data = {}

    _initialize_client_from_environment()
    return _client.create_deposit(data=data, timestamp=timestamp)


def create_withdrawal(data=None, timestamp=None):
    if not data:
        data = {}

    _initialize_client_from_environment()
    return _client.create_withdrawal(data=data, timestamp=timestamp)


def send_bitcoin(data=None, timestamp=None):
    if not data:
        data = {}

    _initialize_client_from_environment()
    return _client.send_bitcoin(data=data, timestamp=timestamp)
