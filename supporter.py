import csv
import datetime


class Supporter:
    def __init__(self, exchange, history_file=None):
        self._exchange = exchange
        # Specify Asset set
        self._assets = ["BOND", "GS", "MS", "VALBZ", "VALE", "WFC", "XLF"]
        # Should Add file location check
        self._history_file = history_file

    def listen(self, message):
        """
        read message and record filled trade
        """

        if message["type"] != "trade" and message["sym"] not in self._assets:
            return

        new_row = [datetime.datetime.now(), message["price"]]

        with open(str(message["sym"] + self._history_file), "a") as fd:
            writer_object = csv.writer(fd)
            writer_object.writerow(new_row)
            fd.close()
