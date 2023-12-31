import math
from jane_street import Dir


# class Arbitrage:
#     def __init__(self, exchange):
#         self._exchange = exchange
#         self._assets = ["VALE", "VALBZ"]

#         # self._xlfs = ["XLF", "BOND", "GS", "MS", "WFC"]

#         self._base_id = 1_000_000
#         self._oid = {}
#         self._valPrices = {}
#         for asset in self._assets:
#             self._valPrices[asset] = 0

#             self._oid[asset + "B"] = self._base_id + 1
#             self._oid[asset + "C"] = self._base_id + 2
#             self._oid[asset + "S"] = self._base_id + 3
#             self._base_id += 3

#         self._totalEarn = 0

#     def listen(self, msg):
#         if msg["type"] != "trade" or msg["symbol"] not in self._assets:
#             return

#         symbol = msg["symbol"]
#         price = msg["price"]

#         # if self._valPrices["BOND"] != 0 and self._valPrices["GS"] != 0 and self._valPrices["MS"] != 0 and self._valPrices["WFC"] != 0:
#         #     xlfStockPrices = 3 * self._valPrices["BOND"] + 2 * self._valPrices["GS"] + \
#         #         3 * self._valPrices["MS"] + 2 * self._valPrices["WFC"]

#         buy_id = self._oid[symbol + "B"]
#         convert_id = self._oid[symbol + "C"]
#         sell_id = self._oid[symbol + "S"]

#         self._valPrices[symbol] = price

#         # if self._valPrices["XLF"] - xlfStockPrices > 100:

#         if self._valPrices["VALE"] - self._valPrices["VALBZ"] > 10:
#             self._exchange.send_add_message(
#                 order_id=buy_id, symbol="VALBZ", dir=Dir.BUY, price=self._valPrices["VALBZ"], size=50)
#             self._exchange.send_convert_message(
#                 order_id=convert_id, symbol="VALBZ", dir=Dir.BUY, size=50)
#             self._exchange.send_add_message(
#                 order_id=sell_id, symbol="VALE", dir=Dir.SELL, price=self._valPrices["VALE"], size=50)
#             self._totalEarn += (self._valPrices["VALE"] -
#                                 self._valPrices["VALBZ"] - 10)

#         if self._valPrices["VALBZ"] - self._valPrices["VALE"] > 10:
#             self._exchange.send_add_message(
#                 order_id=buy_id, symbol="VALE", dir=Dir.BUY, price=self._valPrices["VALE"], size=50)
#             self._exchange.send_convert_message(
#                 order_id=convert_id, symbol="VALE", dir=Dir.BUY, size=50)
#             self._exchange.send_add_message(
#                 order_id=sell_id, symbol="VALBZ", dir=Dir.SELL, price=self._valPrices["VALBZ"], size=50)
#             self._totalEarn += (self._valPrices["VALBZ"] -
#                                 self._valPrices["VALE"] - 10)

#         print("TOTAL ARBITRAGE EARN:", self._totalEarn)
