import collections
import pandas as pd
import pandas_datareader.data as web
from .event import Bar


class DataSource:
    """
    DataSource is a base class for market data
    """

    def get_next(self):
        pass


class YahooDataSource(DataSource):
    """
    YahooDataSource is an implementation of DataSource that scrapes data from yahoo
    """

    def __init__(self, tickers, start, end, event_queue):
        self.tickers = tickers
        self.event_queue = event_queue
        self.continue_running = True

        self._last_close = {}
        self._last_adj_close = {}
        self._last_timestamp = {}

        data = {}
        for ticker in tickers:
            data[ticker] = web.DataReader(ticker, "yahoo", start, end)
            # add ticker column to data
            data[ticker]["Ticker"] = ticker
        self.df = pd.concat(data.values()).sort_index()
        self.stream = self._stream_events()

    def _stream_events(self):
        return self.df.iterrows()

    def last_close(self, ticker):
        return self._last_close.get(ticker, None)

    def last_adj_close(self, ticker):
        return self._last_adj_close.get(ticker, None)

    def last_timestamp(self, ticker):
        return self._last_timestamp.get(ticker, None)

    def get_next(self):
        try:
            time, row = next(self.stream)
        except StopIteration:
            self.continue_running = False
            return
        self.event_queue.put(
            Bar(
                row["Ticker"],
                time,
                86400,
                row["Open"],
                row["High"],
                row["Low"],
                row["Close"],
                row["Volume"],
                row["Adj Close"],
            )
        )
        self._last_close[row["Ticker"]] = row["Close"]
        self._last_adj_close[row["Ticker"]] = row["Adj Close"]
        self._last_timestamp[row["Ticker"]] = time

