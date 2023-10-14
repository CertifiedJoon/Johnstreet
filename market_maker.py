from enum import Enum
from jane_street import ExchangeConnection as Exchange
from jane_street import Dir


class MarketMaker:
    def __init__(self, exchange, delta):
        self._exchange = exchange
        self._base_id = 1_000_000
        self._delta = delta
        self._assets = ["BOND", "GS", "MS", "VALBZ", "VALE", "WFC", "XLF"]
        self._oid = {}
        for asset in self._assets:
            self._oid[asset + "B"] = self._base_id + 1
            self._oid[asset + "S"] = self._base_id + 2
            self._base_id += 2

    def listen(self, msg):
        if msg["type"] != "trade" or msg["symbol"] not in self._assets:
            return

        sym = msg["symbol"]
        prc = msg["price"]

        buy_price = prc - self._delta
        sell_price = prc + 1

        buy_id = self._oid[sym + "B"]
        sell_id = self._oid[sym + "S"]

        print(f"liquity providing at {sym} {prc}")
        self._exchange.send_cancel_message(order_id=buy_id)
        self._exchange.send_cancel_message(order_id=sell_id)

        self._exchange.send_add_message(
            order_id=buy_id, symbol=sym, dir=Dir.BUY, price=buy_price, size=1
        )
        self._exchange.send_add_message(
            order_id=sell_id, symbol=sym, dir=Dir.SELL, price=sell_price, size=1
        )
