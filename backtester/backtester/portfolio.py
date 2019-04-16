class Portfolio:
    def __init__(self, data_source, cash):
        self.data_source = data_source
        self.cash = cash
        self.positions = {}

    @property
    def equity(self):
        value = self.cash
        for ticker, quantity in self.positions.items():
            value += self.data_source.last_close(ticker) * quantity
        return value

    def fill_order(self, fill):
        self.cash -= (fill.quantity * fill.fill_price) + fill.commission
        self.positions[fill.ticker] = fill.quantity + self.positions.get(fill.ticker, 0)

