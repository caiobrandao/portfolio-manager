
import os
import sys

from scripts.portfolio.position import Portfolio

from portfolio.transactions import Transaction

from historical_data.provider import Provider

from asset.equities import EquityAsset

provider = Provider()
provider.search_prices('MGLU3')
print(provider.get_prices())