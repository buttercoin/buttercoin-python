Buttercoin Python SDK Client
===============

Official Python Client of the Buttercoin API.  Buttercoin is a trading platform that makes buying and selling bitcoin easy.

### Getting Started

Use pip to install:

```python
pip install buttercoin
```

### Examples

#### Initialization

Setting | Property Name | Description
--- | --- | ---
API Key | `apiKey` | Your Buttercoin API Key
API Secret | `apiSecret` | Your Buttercoin API Secret
Mode | `mode` | Your development environment (default: `'production'`, set to `'sandbox'` to test with testnet bitcoins)

```python
from buttercoin.client import ButtercoinClient

client = ButtercoinClient(
                public_key='<BUTTERCOIN_API_KEY>',
                secret_key='<BUTTERCOIN_API_SECRET>',
                mode='<BUTTERCOIN_MODE>' # production or sandbox
         )
```

#### Tips

A note on the `timestamp` param sent to all client methods:
This param must always be increasing, and within 5 minutes of Buttercoin server times (GMT). This is to prevent replay attacks on your data.

Because of this, if you need your API calls to run in a certain order, you must chain together callbacks to ensure synchronous responses to your requests.

*Additionally, for convenience, if you don't include the timestamp parameter, it will default to the current timestamp.*

```
timestamp = unicode(int(round(time.time() * 1000)))

client.get_key(timestamp=timestamp)

# or default to current timestamp

client.get_key()
```

#### Get Data

**Key Permissions**  
Returns `array` of permissions associated with this key

```python
client.get_key()
```

**Balances**  
Returns `dict` of balances for this account

```python
client.get_balances()
```

**Deposit Address**  
Returns bitcoin address `string` to deposit your funds into the Buttercoin platform

```python
client.get_deposit_address()
```

**Get Orders**  
Returns `array` of `dict` objects containing information about buy and sell orders

Name | Param | Description
--- | --- | ---
Status | `status` | enum: `['opened', 'partial-filled', 'filled', 'canceled']`  
Side | `side` | enum: `['buy', 'sell']`  
Order Type | `orderType` | enum: `['market', 'limit']`  
Date Min | `dateMin` | format: ISO-8601, e.g. `'2014-05-06T13:15:30Z'`  
Date Max | `dateMax` | format: ISO-8601, e.g. `'2014-05-06T13:15:30Z'`  

```python
# query for multiple orders
body = {'status':'canceled'}
client.get_orders(body=body)

# single order by id
client.get_order_by_id('<order_id>');

# single order by url
client.get_order_by_url('http://api.buttercoin.com/v1/orders/b9fa58e6-a441-48ca-afbb-14827fca2f7a')
```

**Get Transactions**  
Returns `array` of `dict` objects containing information about deposit and withdraw action

Name | Param | Description
--- | --- | ---
Status | `status` | enum: `['pending', 'processing', 'funded', 'canceled', 'failed']`  
Transaction Type | `transactionType` | enum: `['deposit', 'withdrawal']`  
Date Min | `dateMin` | format: ISO-8601, e.g. `'2014-05-06T13:15:30Z'`  
Date Max | `dateMax` | format: ISO-8601, e.g. `'2014-05-06T13:15:30Z'`  

```python
# query for multiple transactions
body = {'status':'pending'}
client.get_transactions(body=body)

# single transaction by id
client.get_transaction_by_id('<transaction_id>');

# single transaction by url
client.get_transaction_by_url('http://api.buttercoin.com/v1/transactions/53db06ee7400007700f4c561')
});
```

###### Unauthenticated Requests (not subject to daily API rate limit)

**Get Order Book**  
Return a `dict` object of current orders in the Buttercoin order book

```python
client.get_order_book()
```

**Get Ticker**  
Return the current bid, ask, and last sell prices on the Buttercoin platform

```python
client.get_ticker()
```

#### Create New Actions

**Create Order**

Valid order params include:

Name | Param | Description
--- | --- | ---
Instrument | `instrument` | enum: `['BTC_USD, USD_BTC']`
Side | `side` | enum: `['buy', 'sell']`, required `true`  
Order Type | `orderType` | enum: `['limit', 'market']`, required `true`  
Price | `price` | `string`, required `false`  
Quantity | `quantity` | `string`, required `false`

```python
# create a JSON object with the following params
order = {"instrument":"BTC_USD","side": "buy","orderType":"limit","price":"600","quantity":"0.2346"}

client.create_order(body=order) # http://api.buttercoin.com/v1/orders/b9fa58e6-a441-48ca-afbb-14827fca2f7a
```

**Create Transaction**  

Deposit transaction params include:  

Name | Param | Description
--- | --- | ---
Method | `method` | enum: `['wire']`, required `true`  
Currency | `currency` | enum: `['USD']`, required `true`  
Amount | `amount` | `string`, required `true`  

```python
# create deposit
txn = { "method": "wire", "currency": "USD", "amount": "500" }
client.create_deposit(body=txn) # https://api.buttercoin.com/v1/transactions/53db06ee7400007700f4c561
```

Withdrawal transaction params include:  

Name | Param | Description
--- | --- | --- 
Method | `method` | enum: `['check']`, required `true`  
Currency | `currency` | enum: `['USD']`, required `true`  
Amount | `amount` | `string`, required `true`

*If you have the security setting requiring confirmation of dollar withdrawals, you will see a 201 status*

```python
# create withdrawal
txn = { "currency": "USD", "amount": "30020.30", "method": "check" } 
json = client.create_withdrawal(body=txn) # https://api.buttercoin.com/v1/transactions/53db06ee7400007700f4c561

```
Send bitcoin transaction params include:  

Name | Param | Description
--- | --- | --- 
Currency | `currency` | `['USD']`, required `true`  
Amount | `amount` | `string`, required `true`  
Destination | `destination` | address to which to send currency `string`, required `true`

*If you have the security setting requiring confirmation of bitcoin withdrawals, you will see a 201 status*

```python
# send bitcoins to an address
txn = { "currency": "BTC", "amount": "0.30", "destination": "msj42CCGruhRsFrGATiUuh25dtxYtnpbTx" } 
json = client.send_bitcoin(body=txn) # https://api.buttercoin.com/v1/transactions/53db06ee7400007700f4c561
```


#### Cancel Actions

All successful cancel calls to the API return a response status of `204` with a human readable success message

**Cancel Order**  
Cancel a pending buy or sell order

```python
client.cancel_order('<order_id>')
```

**Cancel Transaction**  
Cancel a pending deposit or withdraw action

```python
client.cancel_transaction('<transaction_id>')
```

### Further Reading

[Buttercoin - Website](https://www.buttercoin.com)  
[Buttercoin API Docs](https://developer.buttercoin.com)

### Contributing

This is an open source project and we love involvement from the community! Hit us up with pull requests and issues. 

### Release History

#### 0.0.1

- First release.

#### 0.0.3

- Changed test env to sandbox

#### 0.0.4

- Some cleanup and aligned naming conventions.

### License

Licensed under the MIT license.