import pandas as pd


class Supporter:
    __slots__ = "_ticker", "_history", "_df", "_strategy"

    def __init__(self, ticker=None, history_file=None):
        """
        Initiates Trader,
        Instanciates _strategy using parameterized factory method
        """
        if self.is_ticker_valid(ticker):
            raise RuntimeError(f"{ticker} is not available.\n")
        self._ticker = ticker
        # Should Add file location check
        self._history_file = history_file
        self._df = pd.read_csv(history_file).set_index("Date")

    def is_ticker_valid(self, ticker):
        raise NotImplementedError("Sorry, not implemented yet!")

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

    def get_ask_price(self):
        """Return the current lowest ask price of _ticker"""
        raise NotImplementedError("Sorry, not implemented yet.")

    def get_bid_price(self):
        """Return the current highest bid price of _ticker"""
        raise NotImplementedError("Sorry, not implemented yet.")

    def get_balance(self):
        """Return balance in client's wallet"""
        raise NotImplementedError("Sorry, not implemented yet.")
