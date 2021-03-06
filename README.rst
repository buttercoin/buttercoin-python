Buttercoin API Python Client
============================

Official Python Client of the `Buttercoin API <https://developer.buttercoin.com>`_.
`Buttercoin <https://buttercoin.com>`_ is a trading platform that makes
buying and selling `bitcoin <http://en.wikipedia.org/wiki/Bitcoin>`_ easy.

Installation
------------

Install via `pip <http://www.pip-installer.org/>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

    $ pip install buttercoin

Install from source
^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

    $ git clone git@github.com:buttercoin/buttercoin-python.git
    $ cd buttercoin-python
    $ python setup.py install

Usage
-----

HMAC-SHA256 Authentication
^^^^^^^^^^^^^^^^^^^^^^^^^^

You need an `API key and secret <https://buttercoin.com/#/api>`_ to use
`HMAC <http://en.wikipedia.org/wiki/Hash-based_message_authentication_code>`_.

+--------------+------------------+----------------------------------------------------------------------------------------------------------------+
| Setting      | Property Name    | Description                                                                                                    |
+==============+==================+================================================================================================================+
| API Key      | ``api_key``      | Your Buttercoin API Key                                                                                        |
+--------------+------------------+----------------------------------------------------------------------------------------------------------------+
| API Secret   | ``api_secret``   | Your Buttercoin API Secret                                                                                     |
+--------------+------------------+----------------------------------------------------------------------------------------------------------------+
| Mode         | ``mode``         | Your development environment (default: ``'production'``, set to ``'sandbox'`` to test with testnet bitcoins)   |
+--------------+------------------+----------------------------------------------------------------------------------------------------------------+

.. code-block:: python

    from buttercoin.client import ButtercoinClient

    client = ButtercoinClient(
        api_key='<BUTTERCOIN_API_KEY>',
        api_secret='<BUTTERCOIN_API_SECRET>',
        mode='<BUTTERCOIN_MODE>' # production or sandbox
    )

Tips
^^^^

A note on the ``timestamp`` param sent to all client methods: This param
must always be increasing, and within 5 minutes of Buttercoin server
times (GMT). This is to prevent replay attacks on your data.

Because of this, if you need your API calls to run in a certain order,
you must chain together callbacks to ensure synchronous responses to
your requests.

*Additionally, for convenience, if you don't include the timestamp
parameter, it will default to the current timestamp.*

::

    timestamp = unicode(int(round(time.time() * 1000)))
    client.get_key(timestamp=timestamp)

    # or default to current timestamp

    client.get_key()

Get Data
^^^^^^^^

Key Permissions
^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns ``array`` of permissions associated with this key.

.. code-block:: python

    client.get_key()

Balances
^^^^^^^^

Returns ``dict`` of balances for this account.

.. code-block:: python

    client.get_balances()

Deposit Address
^^^^^^^^^^^^^^^

Returns bitcoin address ``string`` to deposit your funds into the Buttercoin platform.

.. code-block:: python

    client.get_deposit_address()

Get Orders
^^^^^^^^^^

Returns ``array`` of ``dict`` objects containing information about buy and sell orders.

+--------------+-----------------+----------------------------------------------------------------+
| Name         | Param           | Description                                                    |
+==============+=================+================================================================+
| Status       | ``status``      | enum: ``['opened', 'partial-filled', 'filled', 'canceled']``   |
+--------------+-----------------+----------------------------------------------------------------+
| Side         | ``side``        | enum: ``['buy', 'sell']``                                      |
+--------------+-----------------+----------------------------------------------------------------+
| Order Type   | ``orderType``   | enum: ``['market', 'limit']``                                  |
+--------------+-----------------+----------------------------------------------------------------+
| Date Min     | ``dateMin``     | format: ISO-8601, e.g. ``'2014-05-06T13:15:30Z'``              |
+--------------+-----------------+----------------------------------------------------------------+
| Date Max     | ``dateMax``     | format: ISO-8601, e.g. ``'2014-05-06T13:15:30Z'``              |
+--------------+-----------------+----------------------------------------------------------------+

.. code-block:: python

    # query for multiple orders
    body = {'status':'canceled'}
    client.get_orders(body=body)

    # single order by id
    client.get_order_by_id('<order_id>');

    # single order by url
    client.get_order_by_url('http://api.buttercoin.com/v1/orders/b9fa58e6-a441-48ca-afbb-14827fca2f7a')

Get Transactions
^^^^^^^^^^^^^^^^

Returns ``array`` of ``dict`` objects containing information about deposit and withdraw action.

+--------------------+-----------------------+-----------------------------------------------------------------------+
| Name               | Param                 | Description                                                           |
+====================+=======================+=======================================================================+
| Status             | ``status``            | enum: ``['pending', 'processing', 'funded', 'canceled', 'failed']``   |
+--------------------+-----------------------+-----------------------------------------------------------------------+
| Transaction Type   | ``transactionType``   | enum: ``['deposit', 'withdrawal']``                                   |
+--------------------+-----------------------+-----------------------------------------------------------------------+
| Date Min           | ``dateMin``           | format: ISO-8601, e.g. ``'2014-05-06T13:15:30Z'``                     |
+--------------------+-----------------------+-----------------------------------------------------------------------+
| Date Max           | ``dateMax``           | format: ISO-8601, e.g. ``'2014-05-06T13:15:30Z'``                     |
+--------------------+-----------------------+-----------------------------------------------------------------------+

.. code-block:: python

    # query for multiple transactions
    body = {'status':'pending'}
    client.get_transactions(body=body)

    # single transaction by id
    client.get_transaction_by_id('<transaction_id>');

    # single transaction by url
    client.get_transaction_by_url('http://api.buttercoin.com/v1/transactions/53db06ee7400007700f4c561')
    });

Unauthenticated Requests
------------------------

Get Order Book
^^^^^^^^^^^^^^

Return a ``dict`` object of current orders in the Buttercoin order book.

.. code-block:: python

    client.get_order_book()

Get Ticker
^^^^^^^^^^

Return the current bid, ask, and last sell prices on the Buttercoin platform.

.. code-block:: python

    client.get_ticker()

Get Trade History
^^^^^^^^^^^^^^^^^

Return the last 100 trades.

.. code-block:: python

    client.get_trade_history()

Create New Actions
~~~~~~~~~~~~~~~~~~

Create Order
^^^^^^^^^^^^

Valid order params include:

+--------------+------------------+----------------------------------------------------+
| Name         | Param            | Description                                        |
+==============+==================+====================================================+
| Instrument   | ``instrument``   | enum: ``['BTC_USD, USD_BTC']``                     |
+--------------+------------------+----------------------------------------------------+
| Side         | ``side``         | enum: ``['buy', 'sell']``, required ``true``       |
+--------------+------------------+----------------------------------------------------+
| Order Type   | ``orderType``    | enum: ``['limit', 'market']``, required ``true``   |
+--------------+------------------+----------------------------------------------------+
| Price        | ``price``        | ``string``, required ``false``                     |
+--------------+------------------+----------------------------------------------------+
| Quantity     | ``quantity``     | ``string``, required ``false``                     |
+--------------+------------------+----------------------------------------------------+

.. code-block:: python

    # create a JSON object with the following params
    order = {"instrument":"BTC_USD","side": "buy","orderType":"limit","price":"600","quantity":"0.2346"}

    client.create_order(body=order) # http://api.buttercoin.com/v1/orders/b9fa58e6-a441-48ca-afbb-14827fca2f7a

Create Transaction
^^^^^^^^^^^^^^^^^^

Please contact Buttercoin support before creating a USD deposit using the API.

Deposit transaction params include:

+------------+----------------+-----------------------------------------+
| Name       | Param          | Description                             |
+============+================+=========================================+
| Method     | ``method``     | enum: ``['wire']``, required ``true``   |
+------------+----------------+-----------------------------------------+
| Currency   | ``currency``   | enum: ``['USD']``, required ``true``    |
+------------+----------------+-----------------------------------------+
| Amount     | ``amount``     | ``string``, required ``true``           |
+------------+----------------+-----------------------------------------+

.. code-block:: python

    # create deposit
    txn = { "method": "wire", "currency": "USD", "amount": "500" }
    client.create_deposit(body=txn) # https://api.buttercoin.com/v1/transactions/53db06ee7400007700f4c561

Withdrawal transaction params include:

+------------+----------------+------------------------------------------+
| Name       | Param          | Description                              |
+============+================+==========================================+
| Method     | ``method``     | enum: ``['check']``, required ``true``   |
+------------+----------------+------------------------------------------+
| Currency   | ``currency``   | enum: ``['USD']``, required ``true``     |
+------------+----------------+------------------------------------------+
| Amount     | ``amount``     | ``string``, required ``true``            |
+------------+----------------+------------------------------------------+

If you have the security setting requiring confirmation of dollar withdrawals, you will see a 201 status.

.. code-block:: python

    # create withdrawal
    txn = { "currency": "USD", "amount": "3020.30", "method": "check" }
    json = client.create_withdrawal(body=txn) # https://api.buttercoin.com/v1/transactions/53db06ee7400007700f4c561

Send bitcoin transaction params include:

+---------------+-------------------+-------------------------------------------------------------------+
| Name          | Param             | Description                                                       |
+===============+===================+===================================================================+
| Currency      | ``currency``      | ``['USD']``, required ``true``                                    |
+---------------+-------------------+-------------------------------------------------------------------+
| Amount        | ``amount``        | ``string``, required ``true``                                     |
+---------------+-------------------+-------------------------------------------------------------------+
| Destination   | ``destination``   | address to which to send currency ``string``, required ``true``   |
+---------------+-------------------+-------------------------------------------------------------------+

*If you have the security setting requiring confirmation of bitcoin
withdrawals, you will see a 201 status*

.. code-block:: python

    # send bitcoins to an address
    txn = { "currency": "BTC", "amount": "0.30", "destination": "msj42CCGruhRsFrGATiUuh25dtxYtnpbTx" } 
    json = client.send_bitcoin(body=txn) # https://api.buttercoin.com/v1/transactions/53db06ee7400007700f4c561

Cancel Actions
^^^^^^^^^^^^^^

All successful cancel calls to the API return a response status of
``204`` with a human readable success message

Cancel Order
^^^^^^^^^^^^

Cancel a pending buy or sell order

.. code-block:: python

    client.cancel_order('<order_id>')

Cancel Transaction
^^^^^^^^^^^^^^^^^^

Cancel a pending deposit or withdraw action

.. code-block:: python

    client.cancel_transaction('<transaction_id>')

Further Reading
---------------

-  `Buttercoin - Website <https://www.buttercoin.com>`_
-  `Buttercoin API Documentation <https://developer.buttercoin.com>`_

License
-------

Licensed under the MIT license.

Copyright 2015 `Buttercoin Inc <mailto:hello@buttercoin.com>`_. All Rights Reserved.