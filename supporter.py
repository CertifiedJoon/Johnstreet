class Supporter:
    __slots__ = "_ticker", "_history", "_df", "_strategy"

    def __init__(self, exchange, history_file=None):
        self._exchange = exchange
        # Specify Asset set
        self._assets = []
        # Should Add file location check
        self._history_file = history_file

    def listen(self):
        """Fetch Ticker from external API"""
        # info = self.BINANCE.fetch_ticker(self._ticker)
        pass

        # today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        # new_row = [today, info['open'], info['high'], info['low'], info['close'], info['quoteVolume']]

        # with open(self._history_file,'a') as fd:
        #     writer_object = csv.writer(fd)
        #     writer_object.writerow(new_row)
        #     fd.close()

        # self._df.loc[today] = pd.Series(new_row)
