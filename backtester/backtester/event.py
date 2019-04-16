from enum import Enum

EventType = Enum("EventType", "BAR ORDER FILL SIGNAL")


class Event:
    pass


class Bar(Event):
    def __init__(
        self,
        ticker,
        time,
        period,
        open_price,
        high_price,
        low_price,
        close_price,
        volume,
        adj_close=None,
    ):
        self.type = EventType.BAR
        self.ticker = ticker
        self.time = time
        self.period = period
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price
        self.low_price = low_price
        self.volume = volume
        self.adj_close = adj_close

    def __str__(self):
        return f"<Bar {self.ticker} time={self.time} close={self.close_price}>"


class Order(Event):
    def __init__(self, ticker, target_weight=None, quantity=None):
        self.type = EventType.ORDER
        self.ticker = ticker
        self.target_weight = target_weight
        self.quantity = quantity


class Fill(Event):
    def __init__(self, timestamp, ticker, quantity, fill_price, commission):
        self.type = EventType.FILL
        self.timestamp = timestamp
        self.ticker = ticker
        self.quantity = quantity
        self.fill_price = fill_price
        self.commission = commission
