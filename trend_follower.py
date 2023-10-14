from enum import Enum
from collections import deque


class Dir(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class TrendFollower:
    def __init__(self, exchange, mv_window=100):
        self._exchange = exchange
        # base id
        self._BASE_OID = 1_000_000
        # order price delta
        self._delta = 1
        # Specify Asset set
        self._assets = ["BOND", "GS", "MS", "VALBZ", "VALE", "XLF"]
        # mv window
        self._mv_window = mv_window
        # data for each asset
        self._asset_dataset = {}
        for i in self._assets:
            self._asset_dataset[i] = deque()
        # moving average of each asset
        self._asset_mvavg = {}
        for i in self._assets:
            self._asset_mvavg[i] = deque()

        # one unique order id for each asset and side, e.g. 'WFC' and 'B'
        self._oid = {}
        for asset in self._assets:
            self._oid[asset + "B"] = self._BASE_OID + 1
            self._oid[asset + "S"] = self._BASE_OID + 2
            self._BASE_OID += 2

    # return true or false
    def price_trend_up(self, sym):
        if self._asset_mvavg[sym][0] < self._asset_mvavg[sym][1]:
            return True
        else:
            return False

    # listening
    def listen(self, msg):
        if msg["type"] != "trade":
            return

        if msg["symbol"] not in self._assets:
            return

        sym = msg["symbol"]
        prc = msg["price"]

        self._asset_dataset[sym].append(prc)

        # check if the datatset it has is >= moving window
        if len(self._asset_dataset[sym]) < self._mv_window:
            return
        else:
            # calculate the moving average and store in it dictionary
            if len(self._asset_dataset[sym]) > 100:
                self._asset_dataset[sym].popleft()
            self._asset_mvavg[sym].append(
                sum(self._asset_dataset[sym]) / self._mv_window
            )

        # check if there are 10 moving average datasets
        if len(self._asset_mvavg[sym]) < 2:
            return
        elif len(self._asset_mvavg[sym]) > 2:
            self._asset_mvavg[sym].popleft()

        # check if price trend is going down
        if self.price_trend_up(sym):
            s_prc = prc

            s_oid = self._oid[sym + "S"]

            # add new orders
            self._exchange.send_add_message(
                order_id=s_oid, symbol=sym, dir=Dir.SELL, price=s_prc, size=10
            )
            print("SELL at", s_oid, sym, s_prc, 10)
            return

        b_prc = prc

        b_oid = self._oid[sym + "B"]

        # add new orders
        self._exchange.send_add_message(
            order_id=b_oid, symbol=sym, dir=Dir.BUY, price=b_prc, size=10
        )
        print("BUY AT", b_oid, sym, b_prc, 10)
