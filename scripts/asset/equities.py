
from .general import GeneralAsset

class EquityAsset(GeneralAsset):

    def __init__(self,name,quantity,price):
        super().__init__(name, "equity",quantity,price)