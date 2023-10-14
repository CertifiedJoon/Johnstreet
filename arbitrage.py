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
        self._valPrices["traded"] = symbol

        # if math.abs(self._valPrices["VALE"] - self._valPrices["VALBZ"]) > 10:
        #     self._exchange.send_add_message(order_id=buy_id, symbol = symbol, dir = Dir.BUY, price = )

        # if self._valPrice["VALE"] - self._valPrices["VALBZ"] > 10:
        #     self._exchange.send_add_message()

        # if self._valPrice["VALBZ"] - self._valPrice["VALE"] > 10:
        #     self._exchange.send_add_message()

        print("Val price", self._valPrices)
