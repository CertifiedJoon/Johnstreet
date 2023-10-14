import pandas as pd


class Supporter:
    __slots__ = "_ticker", "_history", "_df", "_strategy"

    def __init__(self, exchange, history_file=None):
        self._exchange = exchange
        # base id
        # Specify Asset set
        self._assets = []

        # one unique order id for each asset and side, e.g. 'WFC' and 'B'
        self._oid = {}
        # Should Add file location check
        self._history_file = history_file
        self._df = pd.read_csv(history_file).set_index("Date")

    def update_ohlcv(self):
        """Fetch Ticker from external API"""
        # info = self.BINANCE.fetch_ticker(self._ticker)
        raise NotImplementedError("Sorry, not implemented yet.")

        # today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        # new_row = [today, info['open'], info['high'], info['low'], info['close'], info['quoteVolume']]

        # with open(self._history_file,'a') as fd:
        #     writer_object = csv.writer(fd)
        #     writer_object.writerow(new_row)
        #     fd.close()

        # self._df.loc[today] = pd.Series(new_row)
