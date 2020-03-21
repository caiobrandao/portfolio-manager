from datetime import datetime


class Portfolio():

    def __init__(self, date, positions = [], strategies = [], default_strategy = ''):

        self.date = date
        self.positions = positions
        self.strategies = strategies
        self.default_strategy = default_strategy
    

    def create_strategy(self, strategy_name, default=False):

        self.strategies.append(strategy_name)

        if (default) | (len(self.strategies) == 1):
            self.default_strategy = strategy_name


    def position(self, by=None):
        
        response={}
        if by == ['strategy','asset_class']:
            for strategy in self.strategies:
                all_classes = self.get_classes()
                for classe in all_classes:               
                    response[strategy][classe] = sum( [position['asset'].get_position() for position in self.positions if ((position["asset"].get_class() == classe) & (position["strategy"] == strategy)) ] )
        elif by == 'strategy':
            for strategy in self.strategies:
                response[strategy] = sum( [position['asset'].get_position() for position in self.positions if position["strategy"] == strategy ] )
        elif by == 'asset_class':
            all_classes = self.get_classes()
            for classe in all_classes:
                response[classe] = sum( [position['asset'].get_position() for position in self.positions if position["asset"].get_class() == classe] )
        elif by == 'asset':
            for position in self.positions:
                response['asset'] = position['asset'].get_name()
                response['position'] = position['asset'].get_position()

        return response



    # def wealth(self, by=None):
        
    #     if by_strategy:
    #         portfolio_position = self.position(by_strategy)
    #         wealth = {}
    #         for statregy in portfolio_position.keys():
    #             for classe in statregy.keys():
    #                 wealth[strategy] = wealth[strategy] + portfolio_position[strategy][classe]
    #     else:
    #         portfolio_position = self.position()
    #         wealth = 0
    #         for classe in portfolio_position.keys():
    #             wealth = wealth + portfolio_position[classe]
        
    #     return wealth

    # def apply_transaction(self,transaction):

    #     if 

    
    def get_classes(self):

        classes = [positions['asset'].get_asset_class() for positions in self.positions]
        return list(set(classes))


    # def transaction(self, direction, asset_class):
    
    #     class_filter = asset_class
    #     if asset_class == 'all':
    #         class_filter = self.get_classes()

    #     investment_by_transaction = [transaction.get("amount", 0) for transaction in self.transactions if ((transaction.get("class") in class_filter) & (transaction.get("direction") == direction) & (transaction.get("date") > session_date))]
    #     return sum(investment_by_transaction)

    # def deposit(self, asset_class='all'):

    #     class_filter = asset_class
    #     if asset_class == 'all':
    #         class_filter = self.get_classes()

    #     return self.transaction(direction="deposit", asset_class=class_filter)

    # def withdrawal(self, asset_class='all'):

    #     class_filter = asset_class
    #     if asset_class == 'all':
    #         class_filter = self.get_classes()

    #     return self.transaction(direction="withdrawal", asset_class=class_filter)
    

# pos = [{"class":"equity", "position":7812},{"class": "bond", "position": 789413},{"class": "equity", "position": 3542}]
# portfolio = Portfolio(datetime(2020,3,19), transactions = [], products = pos)
    
# print(portfolio.wealth())
#print(portfolio.get_classes())