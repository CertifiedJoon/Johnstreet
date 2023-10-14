import math
from jane_street import Dir


class Arbitrage:
    def __init__(self, exchange):
        self._exchange = exchange
        self._assets = ["VALE", "VALBZ", "XLF", "GS", "MS", "WFC"]

        self._base_id = 1_000_000
        self._oid = {}
        self._valPrices = {}
        for asset in self._assets:
            self._valPrices[asset] = 0

            self._oid[asset + "B"] = self._base_id + 1
            self._oid[asset + "S"] = self._base_id + 2
            self._base_id += 2

        self._totalEarn = 0

    def listen(self, msg):
        if msg["type"] != "trade" or msg["symbol"] not in self._assets:
            return

        symbol = msg["symbol"]
        price = msg["price"]

        buy_id = self._oid[symbol + "B"]
        sell_id = self._oid[symbol + "S"]

        self._valPrices[symbol] = price

        for asset in self._assets:
            self._exchange.send_add_message(
                order_id=buy_id,
                symbol=f"{asset}",
                dir=Dir.BUY,
                price=self._valPrices[asset],
                size=1
            )
            self._exchange.send_add_message(
                order_id=sell_id,
                symbol=f"{asset}",
                dir=Dir.SELL,
                price=self._valPrices[asset] + 10,
                size=1
            )

        # if self._valPrices["XLF"] - xlfStockPrices > 100:

        # print("TOTAL ARBITRAGE EARN:", self._totalEarn)
