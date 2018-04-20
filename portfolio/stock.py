"""Defining the Stock class."""
from datetime import date as dt
from pandas.tseries.offsets import BDay
from pandas_datareader import data
from ..utils.dates import is_bday
# import pandas as pd
# from os.path import dirname, realpath
# import pdb

class Stock():
    """Create a stock from a ticker, loading data from google."""

    def __init__(self, ticker, start=dt(2016, 1, 1), end=dt.today()):
        """Load historical prices for the ticker.

        :ticker: stock ticker, used to call google data API
        """
        self.ticker = ticker
        self._prices = data.DataReader(ticker, 'google', start, end)

    # @staticmethod
    # def _path():
        # return dirname(realpath(__file__))

    def __repr__(self):
        """Represent the stock by its ticker."""
        return self.ticker

    # def __repr__(self):
        # """Represent the stock by its ticker."""
        # return "Stock({0})".format(self.ticker)

    # def _filter(self, date):
        # pr = self._prices
        # pdb.set_trace()
        # return pr[datetime.strptime(pr["Date"], "%Y-%m-%d") == date]
        
    def close(self, date):
        """Return stock close price for given date."""
        d = date if is_bday(date) else (date - BDay(1)).date() 
        return self._prices.loc[d]["Close"]

    def x_days_low(self, ndays, col):
        """Return filtered price dataset with only the x days low."""
        pr = self._prices
        pr["X Days Low"] = pr[col].rolling(window=ndays, center=False).min()
        return pr[pr["X Days Low"] == pr[col]]

    def __eq__(self, stk):
        return self.ticker == stk.ticker

    def __hash__(self):
        return hash(self.ticker)

stock = Stock('EFA')
stock2 = Stock('EFA')
print(stock == stock2)
y = x + 1

# print(stock.close(dt(2016, 12, 30)))

