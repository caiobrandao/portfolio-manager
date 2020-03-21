
import os
print(os.path.dirname(os.path.abspath(__file__)))

from .position import Portfolio 
from .portfolio.transactions import Transaction

from .historical_data.provider import Provider

from .asset.equities import EquityAsset


provider = Provider()
provider.search_prices('MGLU3')
print(provider.get_prices())