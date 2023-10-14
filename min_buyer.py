from enum import Enum
from jane_street import ExchangeConnection as Exchange
from jane_street import Dir


class MinBuyer:
    def __init__(self, exchange):
        self._exchange = exchange
        self._assets = ["BOND", "GS", "MS", "VALBZ", "VALE", "WFC", "XLF"]
        self._min_price = {
            "BOND": 1000000,
            "GS": 1000000,
            "MS": 1000000,
            "VALBZ": 1000000,
            "VALE": 1000000,
            "WFC": 1000000,
            "XLF": 1000000,
        }
        self._oid = {}
        for asset in self._assets:
            self._oid[asset + "B"] = self._base_id + 1
            self._oid[asset + "S"] = self._base_id + 2
            self._base_id += 2

    def listen(self, msg):
        if msg["type"] != "trade" or msg["symbol"] not in self._assets:
            return

        sym = msg["symbol"]

        self._min_price[msg["symbol"]] = min(
            self._min_price[msg["symbol"]], msg["price"]
        )

        buy_id = self._oid[sym + "B"]

        print(f"min order at " + str(self._min_price))

        self._exchange.send_add_message(
            order_id=buy_id, symbol=sym, dir=Dir.BUY, price=self._min_price, size=1
        )
