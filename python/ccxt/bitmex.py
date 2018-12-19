# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable


class bitmex (Exchange):

    def describe(self):
        return self.deep_extend(super(bitmex, self).describe(), {
            'id': 'bitmex',
            'name': 'BitMEX',
            'countries': ['SC'],  # Seychelles
            'version': 'v1',
            'userAgent': None,
            'rateLimit': 2000,
            'has': {
                'CORS': False,
                'fetchOHLCV': True,
                'withdraw': True,
                'editOrder': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '1h': '1h',
                '1d': '1d',
            },
            'urls': {
                'test': 'https://testnet.bitmex.com',
                'logo': 'https://user-images.githubusercontent.com/1294454/27766319-f653c6e6-5ed4-11e7-933d-f0bc3699ae8f.jpg',
                'api': 'https://www.bitmex.com',
                'www': 'https://www.bitmex.com',
                'doc': [
                    'https://www.bitmex.com/app/apiOverview',
                    'https://github.com/BitMEX/api-connectors/tree/master/official-http',
                ],
                'fees': 'https://www.bitmex.com/app/fees',
                'referral': 'https://www.bitmex.com/register/rm3C16',
            },
            'api': {
                'public': {
                    'get': [
                        'announcement',
                        'announcement/urgent',
                        'funding',
                        'instrument',
                        'instrument/active',
                        'instrument/activeAndIndices',
                        'instrument/activeIntervals',
                        'instrument/compositeIndex',
                        'instrument/indices',
                        'insurance',
                        'leaderboard',
                        'liquidation',
                        'orderBook',
                        'orderBook/L2',
                        'quote',
                        'quote/bucketed',
                        'schema',
                        'schema/websocketHelp',
                        'settlement',
                        'stats',
                        'stats/history',
                        'trade',
                        'trade/bucketed',
                    ],
                },
                'private': {
                    'get': [
                        'apiKey',
                        'chat',
                        'chat/channels',
                        'chat/connected',
                        'execution',
                        'execution/tradeHistory',
                        'notification',
                        'order',
                        'position',
                        'user',
                        'user/affiliateStatus',
                        'user/checkReferralCode',
                        'user/commission',
                        'user/depositAddress',
                        'user/margin',
                        'user/minWithdrawalFee',
                        'user/wallet',
                        'user/walletHistory',
                        'user/walletSummary',
                    ],
                    'post': [
                        'apiKey',
                        'apiKey/disable',
                        'apiKey/enable',
                        'chat',
                        'order',
                        'order/bulk',
                        'order/cancelAllAfter',
                        'order/closePosition',
                        'position/isolate',
                        'position/leverage',
                        'position/riskLimit',
                        'position/transferMargin',
                        'user/cancelWithdrawal',
                        'user/confirmEmail',
                        'user/confirmEnableTFA',
                        'user/confirmWithdrawal',
                        'user/disableTFA',
                        'user/logout',
                        'user/logoutAll',
                        'user/preferences',
                        'user/requestEnableTFA',
                        'user/requestWithdrawal',
                    ],
                    'put': [
                        'order',
                        'order/bulk',
                        'user',
                    ],
                    'delete': [
                        'apiKey',
                        'order',
                        'order/all',
                    ],
                },
            },
            'wsconf': {
                'conx-tpls': {
                    'default': {
                        'type': 'ws',
                        'baseurl': 'wss://www.bitmex.com/realtime',
                    },
                },
                'methodmap': {
                    '_websocketTimeoutSendPing': '_websocketTimeoutSendPing',
                    '_websocketTimeoutRemoveNonce': '_websocketTimeoutRemoveNonce',
                },
                'events': {
                    'ob': {
                        'conx-tpl': 'default',
                        'conx-param': {
                            'url': '{baseurl}',
                            'id': '{id}',
                        },
                    },
                },
            },
            'exceptions': {
                'exact': {
                    'Invalid API Key.': AuthenticationError,
                    'Access Denied': PermissionDenied,
                    'Duplicate clOrdID': InvalidOrder,
                    'Signature not valid': AuthenticationError,
                },
                'broad': {
                    'overloaded': ExchangeNotAvailable,
                    'Account has insufficient Available Balance': InsufficientFunds,
                },
            },
            'options': {
                'api-expires': None,
                'fetchTickerQuotes': False,
            },
        })

    def fetch_markets(self, params={}):
        markets = self.publicGetInstrumentActiveAndIndices()
        result = []
        for p in range(0, len(markets)):
            market = markets[p]
            active = (market['state'] != 'Unlisted')
            id = market['symbol']
            baseId = market['underlying']
            quoteId = market['quoteCurrency']
            type = None
            future = False
            prediction = False
            basequote = baseId + quoteId
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            swap = (id == basequote)
            symbol = id
            if swap:
                type = 'swap'
                symbol = base + '/' + quote
            elif id.find('B_') >= 0:
                prediction = True
                type = 'prediction'
            else:
                future = True
                type = 'future'
            precision = {
                'amount': None,
                'price': None,
            }
            if market['lotSize']:
                precision['amount'] = self.precision_from_string(self.truncate_to_string(market['lotSize'], 16))
            if market['tickSize']:
                precision['price'] = self.precision_from_string(self.truncate_to_string(market['tickSize'], 16))
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': market['lotSize'],
                        'max': market['maxOrderQty'],
                    },
                    'price': {
                        'min': market['tickSize'],
                        'max': market['maxPrice'],
                    },
                },
                'taker': market['takerFee'],
                'maker': market['makerFee'],
                'type': type,
                'spot': False,
                'swap': swap,
                'future': future,
                'prediction': prediction,
                'info': market,
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetUserMargin({'currency': 'all'})
        result = {'info': response}
        for b in range(0, len(response)):
            balance = response[b]
            currency = balance['currency'].upper()
            currency = self.common_currency_code(currency)
            account = {
                'free': balance['availableMargin'],
                'used': 0.0,
                'total': balance['marginBalance'],
            }
            if currency == 'BTC':
                account['free'] = account['free'] * 0.00000001
                account['total'] = account['total'] * 0.00000001
            account['used'] = account['total'] - account['free']
            result[currency] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['depth'] = limit
        orderbook = self.publicGetOrderBookL2(self.extend(request, params))
        result = {
            'bids': [],
            'asks': [],
            'timestamp': None,
            'datetime': None,
            'nonce': None,
        }
        for o in range(0, len(orderbook)):
            order = orderbook[o]
            side = 'asks' if (order['side'] == 'Sell') else 'bids'
            amount = order['size']
            price = order['price']
            result[side].append([price, amount])
        result['bids'] = self.sort_by(result['bids'], 0, True)
        result['asks'] = self.sort_by(result['asks'], 0)
        return result

    def fetch_order(self, id, symbol=None, params={}):
        filter = {'filter': {'orderID': id}}
        result = self.fetch_orders(symbol, None, None, self.deep_extend(filter, params))
        numResults = len(result)
        if numResults == 1:
            return result[0]
        raise OrderNotFound(self.id + ': The order ' + id + ' not found.')

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        request = {}
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if since is not None:
            request['startTime'] = self.iso8601(since)
        if limit is not None:
            request['count'] = limit
        request = self.deep_extend(request, params)
        # why the hassle? urlencode in python is kinda broken for nested dicts.
        # E.g. self.urlencode({"filter": {"open": True}}) will return "filter={'open':+True}"
        # Bitmex doesn't like that. Hence resorting to self hack.
        if 'filter' in request:
            request['filter'] = self.json(request['filter'])
        response = self.privateGetOrder(request)
        return self.parse_orders(response, market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        filter_params = {'filter': {'open': True}}
        return self.fetch_orders(symbol, since, limit, self.deep_extend(filter_params, params))

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        # Bitmex barfs if you set 'open': False in the filter...
        orders = self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 'closed')

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        if not market['active']:
            raise ExchangeError(self.id + ': symbol ' + symbol + ' is delisted')
        request = self.extend({
            'symbol': market['id'],
            'binSize': '1d',
            'partial': True,
            'count': 1,
            'reverse': True,
        }, params)
        bid = None
        ask = None
        if self.options['fetchTickerQuotes']:
            quotes = self.publicGetQuoteBucketed(request)
            quotesLength = len(quotes)
            quote = quotes[quotesLength - 1]
            bid = self.safe_float(quote, 'bidPrice')
            ask = self.safe_float(quote, 'askPrice')
        tickers = self.publicGetTradeBucketed(request)
        ticker = tickers[0]
        timestamp = self.milliseconds()
        open = self.safe_float(ticker, 'open')
        close = self.safe_float(ticker, 'close')
        change = close - open
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': bid,
            'bidVolume': None,
            'ask': ask,
            'askVolume': None,
            'vwap': self.safe_float(ticker, 'vwap'),
            'open': open,
            'close': close,
            'last': close,
            'previousClose': None,
            'change': change,
            'percentage': change / open * 100,
            'average': self.sum(open, close) / 2,
            'baseVolume': self.safe_float(ticker, 'homeNotional'),
            'quoteVolume': self.safe_float(ticker, 'foreignNotional'),
            'info': ticker,
        }

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        timestamp = self.parse8601(ohlcv['timestamp'])
        return [
            timestamp,
            ohlcv['open'],
            ohlcv['high'],
            ohlcv['low'],
            ohlcv['close'],
            ohlcv['volume'],
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        # send JSON key/value pairs, such as {"key": "value"}
        # filter by individual fields and do advanced queries on timestamps
        # filter = {'key': 'value'}
        # send a bare series(e.g. XBU) to nearest expiring contract in that series
        # you can also send a timeframe, e.g. XBU:monthly
        # timeframes: daily, weekly, monthly, quarterly, and biquarterly
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'binSize': self.timeframes[timeframe],
            'partial': True,     # True == include yet-incomplete current bins
            # 'filter': filter,  # filter by individual fields and do advanced queries
            # 'columns': [],    # will return all columns if omitted
            # 'start': 0,       # starting point for results(wtf?)
            # 'reverse': False,  # True == newest first
            # 'endTime': '',    # ending date filter for results
        }
        if limit is not None:
            request['count'] = limit  # default 100, max 500
        # if since is not set, they will return candles starting from 2017-01-01
        if since is not None:
            ymdhms = self.ymdhms(since)
            request['startTime'] = ymdhms  # starting date filter for results
        response = self.publicGetTradeBucketed(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(trade['timestamp'])
        symbol = None
        if market is None:
            if 'symbol' in trade:
                market = self.markets_by_id[trade['symbol']]
        if market:
            symbol = market['symbol']
        return {
            'id': trade['trdMatchID'],
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': None,
            'type': None,
            'side': trade['side'].lower(),
            'price': trade['price'],
            'amount': trade['size'],
        }

    def parse_order_status(self, status):
        statuses = {
            'New': 'open',
            'PartiallyFilled': 'open',
            'Filled': 'closed',
            'DoneForDay': 'open',
            'Canceled': 'canceled',
            'PendingCancel': 'open',
            'PendingNew': 'open',
            'Rejected': 'rejected',
            'Expired': 'expired',
            'Stopped': 'open',
            'Untriggered': 'open',
            'Triggered': 'open',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        status = self.parse_order_status(self.safe_string(order, 'ordStatus'))
        symbol = None
        if market is not None:
            symbol = market['symbol']
        else:
            id = order['symbol']
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
        timestamp = self.parse8601(self.safe_string(order, 'timestamp'))
        lastTradeTimestamp = self.parse8601(self.safe_string(order, 'transactTime'))
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'orderQty')
        filled = self.safe_float(order, 'cumQty', 0.0)
        remaining = None
        if amount is not None:
            if filled is not None:
                remaining = max(amount - filled, 0.0)
        cost = None
        if price is not None:
            if filled is not None:
                cost = price * filled
        result = {
            'info': order,
            'id': str(order['orderID']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': order['ordType'].lower(),
            'side': order['side'].lower(),
            'price': price,
            'amount': amount,
            'cost': cost,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': None,
        }
        return result

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if since is not None:
            request['startTime'] = self.iso8601(since)
        if limit is not None:
            request['count'] = limit
        response = self.publicGetTrade(self.extend(request, params))
        return self.parse_trades(response, market)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
            'side': self.capitalize(side),
            'orderQty': amount,
            'ordType': self.capitalize(type),
        }
        if price is not None:
            request['price'] = price
        response = self.privatePostOrder(self.extend(request, params))
        order = self.parse_order(response)
        id = order['id']
        self.orders[id] = order
        return self.extend({'info': response}, order)

    def edit_order(self, id, symbol, type, side, amount=None, price=None, params={}):
        self.load_markets()
        request = {
            'orderID': id,
        }
        if amount is not None:
            request['orderQty'] = amount
        if price is not None:
            request['price'] = price
        response = self.privatePutOrder(self.extend(request, params))
        order = self.parse_order(response)
        self.orders[order['id']] = order
        return self.extend({'info': response}, order)

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        response = self.privateDeleteOrder(self.extend({'orderID': id}, params))
        order = response[0]
        error = self.safe_string(order, 'error')
        if error is not None:
            if error.find('Unable to cancel order due to existing state') >= 0:
                raise OrderNotFound(self.id + ' cancelOrder() failed: ' + error)
        order = self.parse_order(order)
        self.orders[order['id']] = order
        return self.extend({'info': response}, order)

    def is_fiat(self, currency):
        if currency == 'EUR':
            return True
        if currency == 'PLN':
            return True
        return False

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        # currency = self.currency(code)
        if code != 'BTC':
            raise ExchangeError(self.id + ' supoprts BTC withdrawals only, other currencies coming soon...')
        request = {
            'currency': 'XBt',  # temporarily
            'amount': amount,
            'address': address,
            # 'otpToken': '123456',  # requires if two-factor auth(OTP) is enabled
            # 'fee': 0.001,  # bitcoin network fee
        }
        response = self.privatePostUserRequestWithdrawal(self.extend(request, params))
        return {
            'info': response,
            'id': response['transactID'],
        }

    def handle_errors(self, code, reason, url, method, headers, body, response=None):
        if code == 429:
            raise DDoSProtection(self.id + ' ' + body)
        if code >= 400:
            if body:
                if body[0] == '{':
                    response = json.loads(body)
                    error = self.safe_value(response, 'error', {})
                    message = self.safe_string(error, 'message')
                    feedback = self.id + ' ' + body
                    exact = self.exceptions['exact']
                    if message in exact:
                        raise exact[message](feedback)
                    broad = self.exceptions['broad']
                    broadKey = self.findBroadlyMatchedKey(broad, message)
                    if broadKey is not None:
                        raise broad[broadKey](feedback)
                    if code == 400:
                        raise BadRequest(feedback)
                    raise ExchangeError(feedback)  # unknown message

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        query = '/api' + '/' + self.version + '/' + path
        if method != 'PUT':
            if params:
                query += '?' + self.urlencode(params)
        url = self.urls['api'] + query
        if api == 'private':
            self.check_required_credentials()
            auth = method + query
            expires = self.safe_integer(self.options, 'api-expires')
            nonce = str(self.nonce())
            headers = {
                'Content-Type': 'application/json',
                'api-key': self.apiKey,
            }
            if expires is not None:
                expires = self.sum(self.seconds(), expires)
                expires = str(expires)
                auth += expires
                headers['api-expires'] = expires
            else:
                auth += nonce
                headers['api-nonce'] = nonce
            if method == 'POST' or method == 'PUT':
                if params:
                    body = self.json(params)
                    auth += body
            headers['api-signature'] = self.hmac(self.encode(auth), self.encode(self.secret))
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def _websocket_on_open(self, contextId, websocketOptions):
        lastTimer = self._contextGet(contextId, 'timer')
        if lastTimer is not None:
            self._cancelTimeout(lastTimer)
        lastTimer = self._setTimeout(contextId, 5000, self._websocketMethodMap('_websocketTimeoutSendPing'), [])
        self._contextSet(contextId, 'timer', lastTimer)
        dbids = {}
        self._contextSet(contextId, 'dbids', dbids)
        # send auth
        # nonce = self.nonce()
        # signature = self.hmac(self.encode('GET/realtime' + str(nonce)), self.encode(self.secret))
        # payload = {
        #     'op': 'authKeyExpires',
        #     'args': [self.apiKey, nonce, signature]
        #  }
        # self.asyncSendJson(payload)

    def _websocket_on_message(self, contextId, data):
        # send ping after 5 seconds if not message received
        if data == 'pong':
            return
        msg = json.loads(data)
        table = self.safe_string(msg, 'table')
        subscribe = self.safe_string(msg, 'subscribe')
        unsubscribe = self.safe_string(msg, 'unsubscribe')
        status = self.safe_integer(msg, 'status')
        if subscribe is not None:
            self._websocket_handle_subscription(contextId, 'ob', msg)
        elif unsubscribe is not None:
            self._websocket_handle_unsubscription(contextId, 'ob', msg)
        elif table is not None:
            if table == 'orderBookL2':
                self._websocket_handle_ob(contextId, msg)
        elif status is not None:
            self._websocket_handle_error(contextId, msg)

    def _websocket_timeout_send_ping(self):
        self.websocketSend('ping')

    def _websocket_handle_error(self, contextId, msg):
        status = self.safe_integer(msg, 'status')
        error = self.safe_string(msg, 'error')
        self.emit('err', ExchangeError(self.id + ' status ' + status + ':' + error), contextId)

    def _websocket_handle_subscription(self, contextId, event, msg):
        success = self.safe_value(msg, 'success')
        subscribe = self.safe_string(msg, 'subscribe')
        parts = subscribe.split(':')
        partsLen = len(parts)
        if partsLen == 2:
            if parts[0] == 'orderBookL2':
                symbol = self.find_symbol(parts[1])
                symbolData = self._contextGetSymbolData(contextId, event, symbol)
                if 'sub-nonces' in symbolData:
                    nonces = symbolData['sub-nonces']
                    keys = list(nonces.keys())
                    for i in range(0, len(keys)):
                        nonce = keys[i]
                        self._cancelTimeout(nonces[nonce])
                        self.emit(nonce, success)
                    symbolData['sub-nonces'] = {}
                    self._contextSetSymbolData(contextId, event, symbol, symbolData)

    def _websocket_handle_unsubscription(self, contextId, event, msg):
        success = self.safe_value(msg, 'success')
        unsubscribe = self.safe_string(msg, 'unsubscribe')
        parts = unsubscribe.split(':')
        partsLen = len(parts)
        if partsLen == 2:
            if parts[0] == 'orderBookL2':
                symbol = self.find_symbol(parts[1])
                if success:
                    dbids = self._contextGet(contextId, 'dbids')
                    if symbol in dbids:
                        self.omit(dbids, symbol)
                        self._contextSet(contextId, 'dbids', dbids)
                symbolData = self._contextGetSymbolData(contextId, event, symbol)
                if 'unsub-nonces' in symbolData:
                    nonces = symbolData['unsub-nonces']
                    keys = list(nonces.keys())
                    for i in range(0, len(keys)):
                        nonce = keys[i]
                        self._cancelTimeout(nonces[nonce])
                        self.emit(nonce, success)
                    symbolData['unsub-nonces'] = {}
                    self._contextSetSymbolData(contextId, event, symbol, symbolData)

    def _websocket_handle_ob(self, contextId, msg):
        action = self.safe_string(msg, 'action')
        data = self.safe_value(msg, 'data')
        symbol = self.safe_string(data[0], 'symbol')
        symbol = self.find_symbol(symbol)
        dbids = self._contextGet(contextId, 'dbids')
        symbolData = self._contextGetSymbolData(contextId, 'ob', symbol)
        if action == 'partial':
            ob = {
                'bids': [],
                'asks': [],
                'timestamp': None,
                'datetime': None,
                'nonce': None,
            }
            obIds = {}
            for o in range(0, len(data)):
                order = data[o]
                side = 'asks' if (order['side'] == 'Sell') else 'bids'
                amount = order['size']
                price = order['price']
                priceId = order['id']
                ob[side].append([price, amount])
                obIds[priceId] = price
            ob['bids'] = self.sort_by(ob['bids'], 0, True)
            ob['asks'] = self.sort_by(ob['asks'], 0)
            symbolData['ob'] = ob
            dbids[symbol] = obIds
            self.emit('ob', symbol, self._cloneOrderBook(ob, symbolData['limit']))
        elif action == 'update':
            if symbol in dbids:
                obIds = dbids[symbol]
                curob = symbolData['ob']
                for o in range(0, len(data)):
                    order = data[o]
                    amount = order['size']
                    side = 'asks' if (order['side'] == 'Sell') else 'bids'
                    priceId = order['id']
                    price = obIds[priceId]
                    self.updateBidAsk([price, amount], curob[side], order['side'] == 'Buy')
                symbolData['ob'] = curob
                self.emit('ob', symbol, self._cloneOrderBook(curob, symbolData['limit']))
        elif action == 'insert':
            if symbol in dbids:
                curob = symbolData['ob']
                for o in range(0, len(data)):
                    order = data[o]
                    amount = order['size']
                    side = 'asks' if (order['side'] == 'Sell') else 'bids'
                    priceId = order['id']
                    price = order['price']
                    self.updateBidAsk([price, amount], curob[side], order['side'] == 'Buy')
                    dbids[symbol][priceId] = price
                symbolData['ob'] = curob
                self.emit('ob', symbol, self._cloneOrderBook(curob, symbolData['limit']))
        elif action == 'delete':
            if symbol in dbids:
                obIds = dbids[symbol]
                curob = symbolData['ob']
                for o in range(0, len(data)):
                    order = data[o]
                    side = 'asks' if (order['side'] == 'Sell') else 'bids'
                    priceId = order['id']
                    price = obIds[priceId]
                    self.updateBidAsk([price, 0], curob[side], order['side'] == 'Buy')
                    self.omit(dbids[symbol], priceId)
                symbolData['ob'] = curob
                self.emit('ob', symbol, self._cloneOrderBook(curob, symbolData['limit']))
        else:
            self.emit('err', ExchangeError(self.id + ' invalid orderbook message'))
        self._contextSet(contextId, 'dbids', dbids)
        self._contextSetSymbolData(contextId, 'ob', symbol, symbolData)

    def _websocket_subscribe(self, contextId, event, symbol, nonce, params={}):
        if event != 'ob':
            raise NotSupported('subscribe ' + event + '(' + symbol + ') not supported for exchange ' + self.id)
        id = self.market_id(symbol).upper()
        payload = {
            'op': 'subscribe',
            'args': ['orderBookL2:' + id],
        }
        symbolData = self._contextGetSymbolData(contextId, event, symbol)
        if not('sub-nonces' in list(symbolData.keys())):
            symbolData['sub-nonces'] = {}
        symbolData['limit'] = self.safe_integer(params, 'limit', None)
        nonceStr = str(nonce)
        handle = self._setTimeout(contextId, self.timeout, self._websocketMethodMap('_websocketTimeoutRemoveNonce'), [contextId, nonceStr, event, symbol, 'sub-nonce'])
        symbolData['sub-nonces'][nonceStr] = handle
        self._contextSetSymbolData(contextId, event, symbol, symbolData)
        self.websocketSendJson(payload)

    def _websocket_unsubscribe(self, contextId, event, symbol, nonce, params={}):
        if event != 'ob':
            raise NotSupported('unsubscribe ' + event + '(' + symbol + ') not supported for exchange ' + self.id)
        id = self.market_id(symbol).upper()
        payload = {
            'op': 'unsubscribe',
            'args': ['orderBookL2:' + id],
        }
        symbolData = self._contextGetSymbolData(contextId, event, symbol)
        if not('unsub-nonces' in list(symbolData.keys())):
            symbolData['unsub-nonces'] = {}
        nonceStr = str(nonce)
        handle = self._setTimeout(contextId, self.timeout, self._websocketMethodMap('_websocketTimeoutRemoveNonce'), [contextId, nonceStr, event, symbol, 'unsub-nonces'])
        symbolData['unsub-nonces'][nonceStr] = handle
        self._contextSetSymbolData(contextId, event, symbol, symbolData)
        self.websocketSendJson(payload)

    def _websocket_timeout_remove_nonce(self, contextId, timerNonce, event, symbol, key):
        symbolData = self._contextGetSymbolData(contextId, event, symbol)
        if key in symbolData:
            nonces = symbolData[key]
            if timerNonce in nonces:
                self.omit(symbolData[key], timerNonce)
                self._contextSetSymbolData(contextId, event, symbol, symbolData)

    def _get_current_websocket_orderbook(self, contextId, symbol, limit):
        data = self._contextGetSymbolData(contextId, 'ob', symbol)
        if ('ob' in list(data.keys())) and(data['ob'] is not None):
            return self._cloneOrderBook(data['ob'], limit)
        return None
