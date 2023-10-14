from enum import Enum
from jane_street import ExchangeConnection as Exchange
from jane_street import Dir


class BondBuyer:
    def __init__(self, exchange, delta):
        self._exchange = exchange
        self._base_id = 1_000_000
        self._delta = delta
        self._assets = ["BOND"]
        self._oid = {}
        for asset in self._assets:
            self._oid[asset + "B"] = self._base_id + 1
            self._oid[asset + "S"] = self._base_id + 2
            self._base_id += 2

    def listen(self, msg):
        if msg["type"] != "trade" or msg["symbol"] not in self._assets:
            return

        sym = msg["symbol"]

        buy_price = 1000 - self._delta
        sell_price = 100 + self._delta

        buy_id = self._oid[sym + "B"]
        sell_id = self._oid[sym + "S"]

        print(f"bond order at " + str(buy_price))

        self._exchange.send_add_message(
            order_id=buy_id, symbol=sym, dir=Dir.BUY, price=buy_price, size=1
        )
        self._exchange.send_add_message(
            order_id=sell_id, symbol=sym, dir=Dir.SELL, price=sell_price, size=1
        )
