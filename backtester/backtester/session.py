import queue

from .datasource import YahooDataSource
from .execution import IBSimExecution
from .portfolio import Portfolio
from .event import EventType
from .stats import generate_tearsheet


class Session:
    def __init__(self, equity, start_date, end_date, strategy, event_queue, tickers):
        self.equity = equity
        self.start_date = start_date
        self.end_date = end_date
        self.strategy = strategy
        self.event_queue = event_queue
        self.tickers = tickers

        self.data_source = YahooDataSource(tickers, start_date, end_date, event_queue)
        self.portfolio = Portfolio(self.data_source, equity)
        self.execution = IBSimExecution(event_queue, self.portfolio, self.data_source)

        self.current_time = None
        self.stats = {}

    def _continue_running(self):
        return self.data_source.continue_running

    def _run(self):
        """
        Main event loop
        """
        while self._continue_running():
            try:
                event = self.event_queue.get(False)
            except queue.Empty:
                self.data_source.get_next()
            else:
                print(event)
                if event.type == EventType.BAR:
                    self.current_time = event.time
                    self.strategy.calculate_signals(event)
                    self.stats[event.time] = self.portfolio.equity
                if event.type == EventType.ORDER:
                    self.execution.execute_order(event)
                if event.type == EventType.FILL:
                    self.portfolio.fill_order(event)

    def start(self):
        self._run()
        generate_tearsheet(self.stats)
