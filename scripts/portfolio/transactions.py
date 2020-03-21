


class Transaction():

    def __init__(self,asset,date,quantity,price,cost,operation,strategy,description):

        self.asset = asset
        self.date = date
        self.quanitty = quantity
        self.price = price
        self.cost = cost
        self.operation = operation
        self.strategy = strategy
        self.description = description
        self.amount = self.get_amount()
        self.cash = self.cash_impact
    
    def get_amount(self):

        return self.quanitty * self.price
    
    def cash_impact(self):

        if self.operation == 'buy':
            indicator = -1
        elif self.operation == 'sell':
            indicator = 1

        return indicator * self.get_amount - self.cost