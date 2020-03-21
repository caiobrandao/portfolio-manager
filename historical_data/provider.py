import json
from datetime import datetime

class Provider():
    
    def __init__(self):

        self.prices = None
        self.adj_prices = None
        self.events = None
        self.transactions = None

    def set_events(self,obj):
        self.events = obj
    
    def set_prices(self,obj):
        self.prices = obj

    def set_transactions(self,obj):
        self.transactions = obj

    def get_prices(self):
        return self.prices
    
    def get_events(self):
        return self.events
    
    def get_transactions(self):
        return self.transactions
    
    def get_adj_prices(self):
        return self.adj_prices

    def search_events(self, ticker, start_date=None, end_date=None):
        
        if not start_date:
            start_date = datetime(1900,1,1)
        if not end_date:
            end_date = datetime(2100,1,1) 
        
        headers = ["ticker","date","event_type","price_factor","volume_factor"]
        with open("./db/events.csv", encoding = 'cp1252') as f:
            event_list = []
            for line in f:
                row = line.replace('"','').replace('\n','').split(",")
                if row[0] == ticker + "<XBSP>":
                    row[0] = row[0][0:-6]
                    row[1] = datetime.strptime(row[1], "%Y-%m-%d")
                    row[3] = row[3].replace("-","")
                    if (row[1] >= start_date) & (row[1] <= end_date):
                        if row[3] != "":
                            row[3] = float(row[3])
                            if ('Dividendo' in row[2]) | ('Juros sobre o capital' in row[2]):
                                volume_factor = 1
                            else:
                                volume_factor = 1/row[3]
                            my_dict = dict(zip(headers,[row[0],row[1], row[2], row[3], volume_factor]))
                            event_list.append(my_dict)
        self.set_events(event_list)
        return event_list
    
    def search_prices(self,ticker, start_date=None, end_date=None):
        
        if not start_date:
                start_date = datetime(1900,1,1)
        if not end_date:
            end_date = datetime(2100,1,1) 
        
        headers = ["ticker","date","price"]
        with open("./db/prices.csv", encoding = 'cp1252') as f:
            prices_list = []
            for line in f:
                line = line.replace('"','')
                line = line.replace('\n','')
                row = line.split(",")
                if row[0] == ticker + "<XBSP>":
                    row[0] = row[0][0:-6]
                    row[1] = datetime.strptime(row[1], "%Y-%m-%d")
                    row[2] = row[2].replace("-","")
                    if (row[1] >= start_date) & (row[1] <= end_date):
                        if row[2] != "":
                            row[2] = float(row[2])
                            my_dict = dict(zip(headers, [row[0],row[1], row[2]]))
                            prices_list.append(my_dict)
        self.set_prices(prices_list)
        return prices_list

    def search_transactions(self, start_date=None, end_date=None):
        
        if not start_date:
            start_date = datetime(1900,1,1)
        if not end_date:
            end_date = datetime(2100,1,1) 

        with open("./db/transactions.json", encoding = 'utf-8') as f:
            transactions_list = []
            for line in f:
                try:
                    dict_row = json.loads(line)
                    dict_row["date"] = datetime.strptime(dict_row["date"], "%Y-%m-%d")
                    if (dict_row["date"] >= start_date) & (dict_row["date"] <= end_date):
                        transactions_list.append(dict_row)
                except: 
                    continue
        self.set_transactions(transactions_list)
    
    def order_data(self, data):

        ordered_data = []
        
        if data == 'events':
            last_date = datetime(1900,1,1)
            for event in self.events:
                if event['date'] > last_date:
                    ordered_data.insert(0,event)
                else:
                    ordered_data.insert(len(ordered_data),event)
            
            self.events = ordered_data
        elif data == 'prices':
            last_date = datetime(2100,1,1)
            for price in self.prices:
                if price['date'] < last_date:
                    ordered_data.insert(0,price)
                else:
                    ordered_data.insert(len(ordered_data),price)
            
            self.prices = ordered_data

    def seach_adj_price(self, ticker, start_date=None, end_date=None):

        self.search_events(ticker)
        self.search_prices(ticker)
        self.order_data(data='events')
        self.order_data(data='prices')
        
        cumul_events = []
        last_price_factor = 1
        last_volume_factor = 1
        for event in self.events:
            event['price_factor'] = last_price_factor * event['price_factor']
            event['volume_factor'] = last_volume_factor * event['volume_factor']
            last_price_factor = event['price_factor']
            last_volume_factor = event['volume_factor']
            cumul_events.append(event)
        cumul_events.insert(0,{'date': datetime(2100,1,1), 'event_type': '', 'price_factor': 1, 'volume_factor': 1, 'ticker': ticker})
        cumul_events.insert(len(cumul_events),{'date': datetime(1900,1,1), 'event_type': '', 'price_factor': 0, 'volume_factor': 0, 'ticker': ticker})

        current_event_index = 0
        adj_prices = []
        for price in self.prices:
            if price['date'] <= cumul_events[current_event_index+1]['date']:
                current_event_index = current_event_index+1
            price['price'] = price['price'] * cumul_events[current_event_index]['price_factor']
            adj_prices.append(price)

        self.adj_prices = adj_prices


# provider = Provider()
# provider.seach_adj_price(ticker='MGLU3')
# print(provider.adj_prices)
