class Arbitrage:
    def __init__(self, exchange):
        self.exchange = exchange

        self._assets = ["VALE", "VALBZ"]

        self._valPrices = {}
        for asset in self._assets:
            self._valPrices[asset] = 0

    def listen(self, msg):
        if msg["type"] != "book" or msg["symbol"] not in self._assets:
            return

        symbol = msg["symbol"]
        price = msg["price"]

        self._valPrices[symbol] = price

        print("Val price", self._valPrices)
