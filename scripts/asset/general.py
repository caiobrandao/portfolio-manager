

class GeneralAsset():

    def __init__(self,name,asset_class,quantity,price):

        self.name = name
        self.asset_class = asset_class
        self.quantity = quantity
        self.price = price
        self.position = self.get_position()

    def get_position(self):
    
        return self.quantity * self.price
    
    def get_asset_class(self):

        return self.asset_class
    
    def get_name(self):

        return self.name
