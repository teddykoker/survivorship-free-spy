from .event import Fill


class IBSimExecution:
    def __init__(self, event_queue, portfolio, data_source):
        self.event_queue = event_queue
        self.portfolio = portfolio
        self.data_source = data_source

    def calculate_ib_commission(self, quantity, price):
        return min(0.5 * price * quantity, max(1.0, 0.005 * quantity))

    def execute_order(self, order):
        timestamp = self.data_source.last_timestamp(order.ticker)
        fill_price = self.data_source.last_close(order.ticker)

        if order.target_weight:
            adj_close = self.data_source.last_adj_close(order.ticker)
            dollar_weight = order.target_weight * self.portfolio.equity
            order.quantity = int(dollar_weight // adj_close)

        if order.quantity:
            commission = self.calculate_ib_commission(order.quantity, fill_price)
            fill = Fill(timestamp, order.ticker, order.quantity, fill_price, commission)
            self.event_queue.put(fill)

