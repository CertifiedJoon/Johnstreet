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
        self._assets = []
        # mv window
        self._mv_window = mv_window
        # mv orders
        self._mv_orders = deque()
        # mv avg
        self._mv_avg = deque()

        # one unique order id for each asset and side, e.g. 'WFC' and 'B'
        self._oid = {}
        for asset in self._assets:
            self._oid[asset + "B"] = self._BASE_OID + 1
            self._oid[asset + "S"] = self._BASE_OID + 2
            self._BASE_OID += 2

    def price_trend_up(self, prc):
        if len(self._mv_orders) != self._mv_window:
            self._mv_orders.append(prc)
            return

        popped = self._mv_orders.popleft()
        self._mv_orders.append(prc)

        if len(self._mv_avg) != int(self._mv_window * 0.1):
            self._mv_avg.append(
                (
                    (0 if not self._mv_avg else self._mv_avg[-1]) * self._mv_window
                    - popped
                    + prc
                )
                / self._mv_window
            )
            return

        popped = self._mv_avg.popleft()
        self._mv_avg.append(
            (
                (0 if not self._mv_avg else self._mv_avg[-1]) * self._mv_window
                - popped
                + prc
            )
            / self._mv_window
        )

        return all(
            self._mv_avg[i] < self._mv_avg[i + 1] for i in range(len(self._mv_avg) - 1)
        )

    def listen(self, msg):
        if msg["type"] != "trade":
            return

        if msg["symbol"] not in self._assets:
            return

        sym = msg["symbol"]
        prc = msg["price"]

        if not self.price_trend_up(prc):
            s_prc = prc

            s_oid = self._oid[sym + "S"]

            # add new orders
            self._exchange.send_add_message(
                order_id=s_oid, symbol=sym, dir=Dir.SELL, price=s_prc, size=10
            )
            return

        b_prc = prc

        b_oid = self._oid[sym + "B"]

        # add new orders
        self._exchange.send_add_message(
            order_id=b_oid, symbol=sym, dir=Dir.BUY, price=b_prc, size=10
        )
