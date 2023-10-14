import math
from jane_street import Dir


class Arbitrage:
    def __init__(self, exchange):
        self._exchange = exchange
        self._assets = ["VALE", "VALBZ"]

        self._base_id = 1_000_000
        self._oid = {}
        self._valPrices = {}
        for asset in self._assets:
            self._valPrices[asset] = 0
            self._valPrices["traded"] = ""

            self._oid[asset + "B"] = self._base_id + 1
            self._oid[asset + "S"] = self._base_id + 2
            self._base_id += 2

    def listen(self, msg):
        if msg["type"] != "trade" or msg["symbol"] not in self._assets:
            return

        symbol = msg["symbol"]
        price = msg["price"]

        buy_id = self._oid[symbol + "B"]
        sell_id = self._oid[symbol + "S"]

        self._valPrices[symbol] = price

        if self._valPrice["VALE"] - self._valPrices["VALBZ"] > 10:
            self._exchange.send_add_message(
                order_id=buy_id, symbol="VALBZ", dir=Dir.BUY, price=self._valPrices["VALBZ"], size=1)
            self._exchange.send_add_message(
                order_id=sell_id, symbol="VALE", dir=Dir.SELL, price=self._valPrices["VALE"], size=1)

        if self._valPrice["VALBZ"] - self._valPrice["VALE"] > 10:
            self._exchange.send_add_message(
                order_id=buy_id, symbol="VALE", dir=Dir.BUY, price=self._valPrices["VALE"], size=1)
            self._exchange.send_add_message(
                order_id=sell_id, symbol="VALBZ", dir=Dir.SELL, price=self._valPrices["VALBZ"], size=1)

        print("Val price", self._valPrices)
