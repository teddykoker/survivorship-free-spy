import datetime
import queue

from backtester.event import Order
from backtester.session import Session


class BuyHold:
    def __init__(self, event_queue):
        self.event_queue = event_queue
        self.invested = False

    def on_data(self, event):
        if not self.invested and event.ticker == "UPRO":
            order = Order("UPRO", target_weight=1.0)
            self.event_queue.put(order)
            self.invested = True


def run():
    initial_equity = 10000.0
    start_date = datetime.datetime(2000, 1, 1)
    end_date = datetime.datetime(2019, 1, 1)

    event_queue = queue.Queue()
    backtest = Session(
        equity=initial_equity,
        start_date=start_date,
        end_date=end_date,
        strategy=BuyHold(event_queue),
        event_queue=event_queue,
        tickers=["UPRO", "SPY"],
    )
    backtest.start()


if __name__ == "__main__":
    run()
